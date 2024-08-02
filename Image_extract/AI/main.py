from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import extractData
import compareFace as cp
import os
import s3
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/extract/front', methods=['POST'])
@cross_origin(origins='*')
def detection_info():
    data = request.get_json()
    idCardImgUrl = data["imageUrl"]
    email = data["email"]
    if not s3.checkUrl(idCardImgUrl):
        response = jsonify({
            'message': 'URL request failed with status code 403',
            'success': False
        })
        response.status_code = 403
        return response

    informationCard = extractData.getInfomationIdCard(idCardImgUrl, email)

    if informationCard == False:
        response = jsonify({
            'message': 'URL request failed with status code 403',
            'success': False
        })
        response.status_code = 403
        return response

    if informationCard == "":
        response = jsonify({
            'message': 'Error detection ID Card. Please upload ID card again!',
            'success': False
        })
        response.status_code = 400
        return response
    else:
        infoIdCard = informationCard.split('|')
        print(infoIdCard)
        response = jsonify({
            'data': {
                "idNumber": infoIdCard[0],
                "idNumberOld": infoIdCard[1],
                "fullname": infoIdCard[2],
                "birthday": infoIdCard[3],
                "gender": infoIdCard[4],
                "address": infoIdCard[5],
                "idCardValidDay": infoIdCard[6],
                "qrCodeImage": os.getenv("URL") + email + "/" + os.getenv("QRCODEIMG"),
                "faceImage": os.getenv("URL") + email + "/" + os.getenv("FACEIMG"),
                "idCardImage": os.getenv("URL") + email + "/" + os.getenv("IDCARDIMG")
            },
            'success': True
        })
        response.status_code = 200
        return response

@app.route('/compare/face', methods=['POST','GET'])
@cross_origin(origins='*')
def detection_face():
    data = request.get_json()
    faceIdCardImage = data["imageFaceIdCard"]
    selfieImage = data["selfieImage"]

    compareFace = cp.compareFace(faceIdCardImage, selfieImage)

    if compareFace == False:
        response = jsonify({
            'message': 'URL request failed with status code 403',
            'success': False
        })
        response.status_code = 403
        return response

    if compareFace == None:
        response = jsonify({
            'message': 'No face detected in the Selfie image or Face ID card',
            'success': False
        })
        response.status_code = 403
        return response

    if (float(compareFace) >= 40):
        return jsonify({
            "data": {
                "numberPercent": compareFace,
                "match": True,
            },
            "success": True
        })
    else:
        return jsonify({
            "data": {
                "numberPercent": compareFace,
                "match": False,
            },
            "success": False
        })

@app.route('/healthcheck', methods=['GET'])
def getHealthCheck():
    return jsonify({
        "message": "Server is running",
    })

@app.route('/upload', methods=['POST'])
def uploadImage():
    try:
        data = request.get_json()
        fileContents = data['fileContents']
        email = data['email']
        fileName = data['fileName']
        s3.uploadFileToS3(fileContents, email, fileName)
        return jsonify({'message': 'Image uploaded successfully', 'success': True})
    except Exception as e:
        return jsonify({'error': 'Image upload failed', 'success': False})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='3003')