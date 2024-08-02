import face_recognition
import urllib.request as ur
import s3

def compareFace(imageFaceIdUrl, imageSelfieUrl, tolenrance = 0.5): 
    if not s3.checkUrl(imageFaceIdUrl) or not s3.checkUrl(imageSelfieUrl):
        return False

    imageFaceIdCard = face_recognition.load_image_file(ur.urlopen(imageFaceIdUrl))
    imageSelfie = face_recognition.load_image_file(ur.urlopen(imageSelfieUrl))

    # Check if faces are detected in the images
    faceLocationsFaceIdCard = face_recognition.face_locations(imageFaceIdCard)
    faceLocationsSelfie = face_recognition.face_locations(imageSelfie)

    if len(faceLocationsFaceIdCard) == 0 or len(faceLocationsSelfie) == 0:
        return None

    encodingImgFaceIdCard = face_recognition.face_encodings(imageFaceIdCard, faceLocationsFaceIdCard)[0]
    encodingImgSelfie = face_recognition.face_encodings(imageSelfie, faceLocationsSelfie)[0]
    distance = face_recognition.face_distance([encodingImgFaceIdCard], encodingImgSelfie)[0]

    if distance <= tolenrance:
        return "{:.2f}".format(100 - distance * 100 )
    else:
        return "{:.2f}".format(100 - distance * 100 )