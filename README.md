# Image Processing Flask API Documentation
## Overview

This documentation provides details on how to use the Image Processing API. The API is designed to take an input image, process it using a series of image processing techniques, and return the processed image. The processing includes steps such as histogram equalization, contrast adjustment, inversion, Gaussian blur, and darkness adjustment.

## API Endpoint

The API has one endpoint:

- **Endpoint**: `/process_image`
- **Method**: POST

## Request Format

- The API accepts **POST** requests with JSON payload.
- The payload must include the **base64-encoded** image data under the key `"image"`.

### Example Request

```json
POST /process_image
Content-Type: application/json

{
    "image": "/9j/4AAQSkZJRgABAQEAAAAAAAD/4QAuRXhpZgAATU0AKgAAAAgAAkAAAAMAAAABAAIAAAEABAAEAAEAAAAAAAAAAD/2wBDAAoHBwkHBgoJCAkLCwoMDxkQDw4ODx4WFxIZJCAmJSMgIyIoLTkwKCo2KyIjMkQyNjs9QEBAJjBGS0U+Sjk/QD3/2wBDAQsLCw8NDx0QEB09KSMpPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT3/wAARCAFkAuADASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD/yq/yZyGX/wBoaf8AwSj/AJZJ7/wSx+f8A8qt/5nIWbS1vxZ+0//AKKc6x8o+VP5Ef+ip/wK2z/0wv/ziv8AzJn8j/8Akav8A8Kf/ZA/9Ff8A5kp5/wD8rL/Cniv/kTP/AEr/wCfKO5rUp/JP5Ef+ip/0N+L2z/0wv/AM4r/Plb8v+FP+8T/5g//AJlfly/ZP+fJv8A5M3/5Gt/8AKP8A/Gn7if2K9F/4KM/5T0/5IyP+KkL/a8h/wDaCf+es/6pTv8A6MtSvQo/1bSvpf8A0W1/wDtNU7q0N+Z+0f+f6Lf8A+PpH8W/kW8L/wCwt8Pf8A8q/+cnI7H3z8yP5uJ/yXn+0/9Gj/APkKxP/AKQqR8w3P8Agon/AME8lDwW8H/gZ/hv/AMAeX2Aooor8uf/2Q=="
}

```

## Response Format

The API returns a JSON response containing the processed image data if the request is successful. If there is an error, an error message is returned.

### Example Successful Response

```json
{
    "success": true,
    "processed_image": "/9j/4AAQSkZJRgABAQEAAAAAAAD/4QAuRXhpZgAATU0AKgAAAAgAAkAAAAMAAAABAAIAAAEABAAEAAEAAAAAAAAAAD/2wBDAAoHBwkHBgoJCAkLCwoMDxkQDw4ODx4WFxIZJCAmJSMgIyIoLTkwKCo2KyIjMkQyNjs9QEBAJjBGS0U+Sjk/QD3/2wBDAQsLCw8NDx0QEB09KSMpPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT3/wAARCAFkAuADASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AA

ECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD/yq/yZyGX/wBoaf8AwSj/AJZJ7/wSx+f8A8qt/5nIWbS1vxZ+0//AKKc6x8o+VP5Ef+ip/wK2z/0wv/ziv8AzJn8j/8Akav8A8Kf/ZA/9Ff8A5kp5/wD8rL/Cniv/kTP/AEr/wCfKO5rUp/JP5Ef+ip/0N+L2z/0wv/AM4r/Plb8v+FP+8T/5g//AJlfly/ZP+fJv8A5M3/5Gt/8AKP8A/Gn7if2K9F/4KM/5T0/5IyP+KkL/a8h/wDaCf+es/6pTv8A6MtSvQo/1bSvpf8A0W1/wDtNU7q0N+Z+0f+f6Lf8A+PpH8W/kW8L/wCwt8Pf8A8q/+cnI7H3z8yP5uJ/yXn+0/9Gj/APkKxP/AKQqR8w3P8Agon/AME8lDwW8H/gZ/hv/AMAeX2Aooor8uf/2Q=="
}

```

### Example Error Response

```json
{
    "error": "No image provided in the request body"
}

```

## Error Handling

If there is an error processing the image or if the request is malformed, the API will return an error message with a corresponding HTTP status code. The error message provides information about the nature of the error.

In case of an internal server error during processing, a generic error message is returned along with a status code of 500.

## Notes

- The processed image is returned in base64-encoded format for ease of inclusion in JSON responses.
- Make sure to include the base64-encoded image data in the request payload under the key `"image"`.
- If the request is successful, the API will return a JSON object with the key `"success"` set to `true` and the processed image data under the key `"processed_image"`.
- If there is an error, the API will return a JSON object with the key `"error"` containing a descriptive error message, and the HTTP status code will reflect the nature of the error (e.g., 400 for client errors, 500 for server errors).

## **Application Output**

### Input image:
![as](https://github.com/AbhilashGaurav/flask_grayscale_image/assets/84313712/fe92e5b8-8ad5-4947-bdbd-6febecdde4a4)



### Output Image:
![received_image](https://github.com/AbhilashGaurav/flask_grayscale_image/assets/84313712/23bd9917-a968-4724-b6b1-701581128f43)

