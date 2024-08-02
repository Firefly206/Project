from deepface import DeepFace
import cv2

def compare_faces_deepface(passport_image_path, person_image_path):
    # Load the images
    passport_image = cv2.imread(passport_image_path)
    person_image = cv2.imread(person_image_path)

    if passport_image is None or person_image is None:
        print("Error: One or both images could not be loaded.")
        return

    # Compare faces using DeepFace
    result = DeepFace.verify(img1_path=passport_image_path, img2_path=person_image_path)

    # Print the result
    if result["verified"]:
        print("The faces are likely of the same person.")
    else:
        print("The faces are likely of different people.")

    #print('Similarity Metric:', result["distance"])

if __name__ == "__main__":
    
    # Paths to the images
    passport_image_path = './media/passport-card-sample.jpg'
    person_image_path = './media/crop_image.jpg'

    # Compare the faces
    compare_faces_deepface(passport_image_path, person_image_path)
