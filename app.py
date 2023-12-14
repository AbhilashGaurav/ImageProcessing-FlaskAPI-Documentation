from flask import Flask, request, jsonify
from PIL import Image
from io import BytesIO
import base64
import cv2
import numpy as np
from scipy.ndimage import gaussian_filter
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
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

@app.route('/process_image', methods=['POST'])
def process_image():
    try:
        # Check if the request contains image data
        if 'image' not in request.json:
            return jsonify({'error': 'No image provided in the request body'}), 400

        # Get the image data from the request
        image_data_base64 = request.json['image']

        # Convert base64-encoded image data to binary
        image_data_binary = base64.b64decode(image_data_base64)

        # Open the image using Pillow (PIL)
        img = Image.open(BytesIO(image_data_binary))

        # Process the image using the preprocess_image function
        processed_image = preprocess_image(img)

        # Convert processed image to base64 for JSON response
        processed_image_base64 = base64.b64encode(cv2.imencode('.png', (processed_image * 255).astype(np.uint8))[1]).decode('utf-8')

        # Return the processed image as a response
        return jsonify({'success': True, 'processed_image': processed_image_base64})
    
    except Exception as e:
        return jsonify({'error': f'Error processing image: {str(e)}'}), 500

# if __name__ == '__main__':
#     app.run(debug=True)
