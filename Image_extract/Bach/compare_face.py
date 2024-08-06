from deepface import DeepFace
import cv2

def compare_faces_deepface(passport_image_path, person_image_path):
    print("Reading images:")
    print("Passport image path:", passport_image_path)
    print("Person image path:", person_image_path)

    # Load the images
    passport_image = cv2.imread(passport_image_path)
    person_image = cv2.imread(person_image_path)

    print("Loaded images:", passport_image is not None, person_image is not None)

    if passport_image is None or person_image is None:
        print("Error: One or both images could not be loaded.")
        return {"error": "One or both images could not be loaded."}

    # Compare faces using DeepFace
    try:
        result = DeepFace.verify(img1_path=passport_image_path, img2_path=person_image_path)
        print("DeepFace result:", result)
    except Exception as e:
        print(f"Error comparing faces: {e}")
        return {"error": str(e)}

    # # Prepare the result
    # if result["verified"]:
    #     result_message = "The faces are likely of the same person."
    # else:
    #     result_message = "The faces are likely of different people."

    # print(result["verified"])
    # return {
    #     "verified": result["verified"]
    # }

    return result["verified"]

if __name__ == "__main__":
    passport_image_path = './media/passport-card-sample.jpg'
    person_image_path = './media/crop_image.jpg'
    print(compare_faces_deepface(passport_image_path, person_image_path))
