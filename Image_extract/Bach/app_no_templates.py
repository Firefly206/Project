from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import os
import time
import requests
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# Import functions 
from compare_face import compare_faces_deepface
from compareFace_Gemini import compare_faces_gemini
from crop_image import detect_and_crop_largest_face
from Extract_information import extract_information_from_image

# Load environment variables
load_dotenv()

# Configure Flask app
app = Flask(__name__)
CORS(app)

# Configure API key and Gemini model
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash-latest')
safety_settings = [
    {'category': HarmCategory.HARM_CATEGORY_HATE_SPEECH, 'threshold': HarmBlockThreshold.BLOCK_NONE},
    {'category': HarmCategory.HARM_CATEGORY_HARASSMENT, 'threshold': HarmBlockThreshold.BLOCK_NONE},
    {'category': HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, 'threshold': HarmBlockThreshold.BLOCK_NONE}
]

@app.route('/upload_image', methods=['POST'])
@cross_origin()
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image part in the request"}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    image_path = './media/' + file.filename
    file.save(image_path)
    return jsonify({"message": f"Image saved to {image_path}"})

@app.route('/upload_image_url', methods=['POST'])
@cross_origin()
def upload_image_url():
    data = request.get_json()
    image_url = data.get('image_url')
    if not image_url:
        return jsonify({"error": "No image URL provided"}), 400

    try:
        response = requests.get(image_url)
        response.raise_for_status()
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 400

    image = Image.open(BytesIO(response.content))
    image_filename = os.path.basename(image_url)
    image_path = os.path.join('./media', image_filename)
    image.save(image_path)

    return jsonify({"message": f"Image saved to {image_path}", "image_path": image_path})

@app.route('/extract_information', methods=['POST'])
@cross_origin()
def extract_information():
    if 'image' not in request.files:
        return jsonify({"error": "No image part in the request"}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    image_path = './media/' + file.filename
    file.save(image_path)
    
    response_text = extract_information_from_image(image_path)
    return jsonify({"text": response_text})

@app.route('/crop_image', methods=['POST'])
@cross_origin()
def crop_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image part in the request"}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    image_path = './media/' + file.filename
    output_path = './media/cropped_' + file.filename
    file.save(image_path)
    
    detect_and_crop_largest_face(image_path, output_path)
    return jsonify({"message": f"Cropped image saved to {output_path}"})

@app.route('/compare_faces', methods=['POST'])
@cross_origin()
def compare_faces():
    try:
        if 'image1' not in request.files or 'image2' not in request.files:
            print("Files not in request")
            return jsonify({"error": "Missing one or both image parts in the request"}), 400

        file1 = request.files['image1']
        file2 = request.files['image2']

        print("Files received:", file1.filename, file2.filename)

        if file1.filename == '' or file2.filename == '':
            print("No selected file(s)")
            return jsonify({"error": "No selected file(s)"}), 400

        # Generate unique filenames with timestamp
        timestamp = int(time.time())
        image_path1 = os.path.join('.\media', f'{timestamp}_{file1.filename}')
        image_path2 = os.path.join('.\media', f'{timestamp}_{file2.filename}')

        # Save the uploaded files
        file1.save(image_path1)
        file2.save(image_path2)

        print("Files saved:", image_path1, image_path2)

        # Call the compare_faces_deepface function with the saved image paths
        compare_faces_deepface_result = compare_faces_deepface(image_path1, image_path2)
        compare_faces_gemini_result = compare_faces_gemini(image_path1, image_path2)

        return jsonify({
            "compare_faces_deepface_result": compare_faces_deepface_result,
            "compare_faces_gemini_result": compare_faces_gemini_result
        })
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    os.makedirs('./media', exist_ok=True)  # Create media directory if it doesn't exist
    app.run(debug=True)
