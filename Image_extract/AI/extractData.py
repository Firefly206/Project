import os
import cv2
import dlib
import numpy as np
from pyzbar.pyzbar import decode
from dotenv import load_dotenv
import urllib.request as ur
import s3
import requests
load_dotenv()

#extractFace
def extractFace(pathImageURL, email):
    response = requests.get(pathImageURL)
    imgUrlContent = response.content

    detector = dlib.get_frontal_face_detector()

    response = ur.urlopen(pathImageURL)
    image_data = response.read()
    nparr = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)


    height = img.shape[0]
    width = img.shape[1]
    img = cv2.resize(img, (1920, int(height*1920/width)))
    gray =cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    # detect the face
    for _,face in enumerate(faces):
        x1, y1 = face.left(), face.top()
        x2, y2 = face.right(), face.bottom()
        cropped_img = img[y1-200:y2+200, x1-100:x2+100]

        image_string = cv2.imencode('.jpg', cropped_img)[1].tostring()
        s3.uploadFileToS3(image_string, email, os.getenv('FACEIMG'))
        s3.uploadFileToS3(imgUrlContent, email, os.getenv('IDCARDIMG'))
        print("save image done")

#extractQrcode
def reOrder(myPoints):
    myPoints = myPoints.reshape((4, 2))
    myPointsNew = np.zeros((4, 1, 2), dtype=np.int32)
    add = myPoints.sum(1)
    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] =myPoints[np.argmax(add)]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] =myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]
    return myPointsNew
def biggestContour(contours):
    biggest = np.array([])
    max_area = 0
    for i in contours:
        area = cv2.contourArea(i)
        if area > 5000:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            if area > max_area and len(approx) == 4:
                biggest = approx
                max_area = area
    return biggest,max_area
def extractQrcode(pathImageURL, email):
    response = ur.urlopen(pathImageURL)
    image_data = response.read()
    nparr = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    height = img.shape[0]
    width = img.shape[1]
    img = cv2.resize(img, (1920, int(height*1920/width)))
    img = img[0:800, 1100:1900]
    heightImg = img.shape[0]
    widthImg = img.shape[1]
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # CONVERT IMAGE TO GRAY SCALE
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1) # ADD GAUSSIAN BLUR
    imgThreshold = cv2.Canny(imgBlur,200,200) # APPLY CANNY BLUR
    kernel = np.ones((5, 5))
    imgDial = cv2.dilate(imgThreshold, kernel, iterations=2) # APPLY DILATION
    imgThreshold = cv2.erode(imgDial, kernel, iterations=1)  # APPLY EROSION
    # FIND ALL COUNTOURS
    contours, _ = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # FIND ALL CONTOURS
    # FIND THE BIGGEST COUNTOUR
    biggest, _ = biggestContour(contours) # FIND THE BIGGEST CONTOUR
    if biggest.size != 0:
        biggest=reOrder(biggest)
        pts1 = np.float32(biggest) # PREPARE POINTS FOR WARP
        print(pts1)
        p = 20
        pts1 = np.float32([
            [[pts1[0][0][0] - p, pts1[0][0][1] - p]], 
            [[pts1[1][0][0] + p, pts1[1][0][1] - p]], 
            [[pts1[2][0][0] - p, pts1[2][0][1] + p]], 
            [[pts1[3][0][0] + p, pts1[3][0][1] + p]]
        ])
        pts2 = np.float32([[0, 0],[widthImg, 0], [0, heightImg],[widthImg, heightImg]]) # PREPARE POINTS FOR WARP
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg))
        img = cv2.cvtColor(imgWarpColored, cv2.COLOR_BGR2RGB)
        
        image_string = cv2.imencode('.jpg', img)[1].tostring()
        s3.uploadFileToS3(image_string, email, os.getenv('QRCODEIMG'))
        print('save qrcode image done')
    else:
        response = s3.deleteFolderS3(email)
        print('cant save qrcode image')
        if not response:
            return False
        return True
        
#scanQrcode
def scanQrcode(email):
    # Download image from URL
    data = ''
    imageQrCodeUrl = os.getenv("URL")+ email + "/" +os.getenv("QRCODEIMG")
    if not s3.checkUrl(imageQrCodeUrl):
        return data
    response = ur.urlopen(imageQrCodeUrl)
    image_data = response.read()
    nparr = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if len(decode(img)) == 0:
        print('No data found')
        data = ''
        s3.deleteFolderS3(email)
    else:
        for barcode in decode(img):
            data = barcode.data.decode('utf-8')
            print("Data:", data)
    return data

#main
def getInfomationIdCard(pathImageURL, email):
    print('\n==========extract face==========')
    extractFace(pathImageURL, email)
    print('\n==========extract qrcode==========')
    extractQrcode(pathImageURL, email)
    print('\n==========scan qrcode==========')
    data = scanQrcode(email)
    if data == '':
        return data
    else:
        return data
