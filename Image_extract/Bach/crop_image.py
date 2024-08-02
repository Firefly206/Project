import cv2

def detect_and_crop_largest_face(image_path, output_path):
    """
    Detects the largest face in an image and crops the region containing the face with some padding.

    Parameters:
    - image_path (str): Path to the input image file.
    - output_path (str): Path to save the cropped image containing the largest face.

    Returns:
    - None
    """
    # Load the image
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Load the pre-trained Haar Cascade classifier for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Find the largest face
    if len(faces) > 0:
        largest_face = max(faces, key=lambda x: x[2] * x[3])
        x, y, w, h = largest_face

        # Crop the region containing the face with some padding
        padding_vertical = (h // 2) - 10
        padding_horizontal = (w // 3) - 10
        x_min = max(0, x - padding_horizontal)
        y_min = max(0, y - padding_vertical)
        x_max = min(image.shape[1], x + w + padding_horizontal)
        y_max = min(image.shape[0], y + h + padding_vertical)

        cropped_region = image[y_min:y_max, x_min:x_max]

        # Save the cropped region to a file
        cv2.imwrite(output_path, cropped_region)
        print(f"Cropped image saved to {output_path}")
    else:
        print("No faces detected in the image.")

        
if __name__ == "__main__":
    image_path = './media/passport-card-sample.jpg'
    output_path = './media/crop_image.jpg'
    detect_and_crop_largest_face(image_path, output_path)
