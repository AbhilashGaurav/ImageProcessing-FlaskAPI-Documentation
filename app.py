from flask import Flask, request, jsonify
from PIL import Image
from io import BytesIO
import base64
import cv2
import numpy as np
from scipy.ndimage import gaussian_filter
from flask_cors import CORS
from flasgger import Swagger
app = Flask(__name__)
CORS(app)
swagger = Swagger(app)
def preprocess_image(image):
    # Convert the PIL Image to a NumPy array
    image = np.array(image)

    # Convert to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    # Apply histogram equalization
    equalized_image = cv2.equalizeHist(gray_image)

    # Create a low contrast image by reducing the contrast
    alpha = 0.5
    low_contrast_image = cv2.addWeighted(gray_image, alpha, equalized_image, 1 - alpha, 0.0)

    # Invert the grayscale image
    invert = cv2.bitwise_not(low_contrast_image)

    # Apply Gaussian blur to smooth the edges
    blur = cv2.GaussianBlur(invert, (21, 21), 0)

    # Invert the blurred image
    invertedblur = cv2.bitwise_not(blur)

    # Divide the grayscale image by the inverted blurred image
    sketch = cv2.divide(low_contrast_image, invertedblur, scale=270.0)

    # Convert to BGR
    colored_sketch = cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)

    # Convert the image to grayscale if it is color
    if colored_sketch.ndim == 3:
        gray_image = np.dot(colored_sketch[..., :3], [0.5, 0.5, 0.8])
    else:
        gray_image = colored_sketch

    # Calculate the average grayscale level of the image
    average_level = np.mean(gray_image)

    # Define the darkness factor (0.0 - 1.0)
    darkness_factor = 0.9

    # Adjust the pixel values to make the image darker
    darkened_image = gray_image - (average_level * darkness_factor)

    # Clip the pixel values to ensure they stay within the valid range [0, 1]
    darkened_image = np.clip(darkened_image, 0, 1)

    # Apply Gaussian blur to the darkened image
    blurred_image = gaussian_filter(darkened_image, sigma=2)

    return blurred_image

# logo add

def overlay_images(logo_bytes, uploaded_img):
    # Open the background image
    bg = Image.open(BytesIO(uploaded_img)).convert("RGBA")

    # Convert the logo bytes to an image object
    logo = Image.open(BytesIO(logo_bytes)).convert("RGBA")

    Ori_width, Ori_height = bg.size
    width = int(Ori_width//20)
    height = int(Ori_height//10)
    logo= logo.resize((height, width))
    # logo.show()
    width,height = logo.size
    pos_w =  Ori_width-width
    pos_h =  Ori_height-height
    # bg.paste(logo,(pos_w,pos_h))

    # Paste the logo onto the background image
    bg.paste(logo, (pos_w, pos_h), logo)

    bg.show()
    # Convert the overlaid image to base64
    overlaid_bytes = BytesIO()
    bg.save(overlaid_bytes, format='PNG')  # Save as PNG to retain transparency
    overlaid_bytes.seek(0)
    base64_image = base64.b64encode(overlaid_bytes.getvalue()).decode()
    return base64_image

# logo calling for base64 image
with open("antim.txt", "r") as file:
    base64_logo = file.read().strip()

@app.route('/process_image', methods=['POST'])
def process_image():
    """
    Process an image and return the result.

    ---
    parameters:
      - name: image
        in: formData
        type: file
        required: true
        description: The image file to be processed.

    responses:
      200:
        description: Successfully processed the image.
        schema:
          properties:
            success:
              type: boolean
              description: Whether the processing was successful.
            processed_image:
              type: string
              description: Base64-encoded processed image data.
      400:
        description: Bad Request. No image provided in the request body.
        schema:
          properties:
            error:
              type: string
              description: Error message.
      500:
        description: Internal Server Error. Error processing the image.
        schema:
          properties:
            error:
              type: string
              description: Error message.
    """
    try:
        # Check if the request contains image data
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided in the request body'}), 400

        # Get the image data from the request
        image_file = request.files['image']

        # Open the image using Pillow (PIL)
        img = Image.open(image_file)

        # Process the image using the preprocess_image function
        processed_image = preprocess_image(img)

        # Convert processed image to base64 for JSON response
        processed_image_base64 = base64.b64encode(cv2.imencode('.png', (processed_image * 255).astype(np.uint8))[1]).decode('utf-8')

        logo = base64.b64decode(base64_logo)
        bg = base64.b64decode(processed_image_base64)
        # Call the function to overlay images and get the base64 result
        base64_result = overlay_images(logo, bg)
        # Return the processed image as a response
        # pr_image = base64.b64encode(cv2.imencode('.png', (base64_result * 255).astype(np.uint8))[1]).decode('utf-8')
        return jsonify({'success': True, 'processed_image': base64_result})
    
    except Exception as e:
        return jsonify({'error': f'Error processing image: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
