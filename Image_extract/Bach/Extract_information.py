import pathlib
import textwrap
import os
from dotenv import load_dotenv

import PIL.Image

import google.generativeai as genai

from google.generativeai.types import HarmCategory, HarmBlockThreshold

load_dotenv()

def extract_information_from_image(image_path):

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

    # Load the image
    img = PIL.Image.open(image_path)

    # Generate response from the model
    response = model.generate_content(
        ['Extract information from image', img],
        safety_settings=safety_settings
    )

    # Print the response text
    print(response.text)
    return response.text

if __name__ == "__main__":
    image_path = './media/passport-card-sample.jpg'
    extract_information_from_image(image_path)

