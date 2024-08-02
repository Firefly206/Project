import pathlib
import textwrap
import os
from dotenv import load_dotenv

import PIL.Image

import google.generativeai as genai


from google.generativeai.types import HarmCategory, HarmBlockThreshold

load_dotenv()

def compare_faces_gemini(image_path1, image_path2):

    # Set API key
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    genai.configure(api_key=GOOGLE_API_KEY)

    # Set Gemini model
    model = genai.GenerativeModel('gemini-1.5-flash-latest')

    # Set safety procedure
    safety_settings = [
        {'category': HarmCategory.HARM_CATEGORY_HATE_SPEECH, 'threshold': HarmBlockThreshold.BLOCK_NONE},
        {'category': HarmCategory.HARM_CATEGORY_HARASSMENT, 'threshold': HarmBlockThreshold.BLOCK_NONE},
        {'category': HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, 'threshold': HarmBlockThreshold.BLOCK_NONE}
    ]

    # Load the images
    img_passport = PIL.Image.open(image_path1)
    img_face = PIL.Image.open(image_path2)

    # Generate response from the model
    response = model.generate_content(
        ['Compare two faces and tell me if they are the same person', img_passport, img_face],
        safety_settings=safety_settings
    )

    # Print the response text
    print(response.text)
    return response.text

if __name__ == "__main__":
    image_passport = './media/passport-card-sample.jpg'
    image_face = './media/crop_image.jpg'
    compare_faces_gemini(image_passport, image_face)
