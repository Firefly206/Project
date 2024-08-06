import pathlib
import textwrap
import os
from dotenv import load_dotenv
import PIL.Image
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

load_dotenv()

def extract_information_from_image(image_path):
    """
    Extracts information from a passport image using Gemini AI.

    Parameters:
    - image_path (str): Path to the input image file.

    Returns:
    - str: Extracted information in structured text format.
    """
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
        ['Extract the following information from this passport image: Passport Number, Nationality, Surname, Given Names, Gender, Date of Birth, Place of Birth, Issued On, Expires On.', img],
        safety_settings=safety_settings
    )

    # Extract and format the text information
    extracted_text = response.text.strip()
    formatted_text = format_passport_information(extracted_text)

    return formatted_text

def format_passport_information(extracted_text):
    """
    Formats the extracted information into a structured text format.

    Parameters:
    - extracted_text (str): The raw extracted text.

    Returns:
    - str: The formatted information as a structured text.
    """
    fields = {
        "Passport Number": "Passport Number: ",
        "Nationality": "Nationality: ",
        "Surname": "Surname: ",
        "Given Names": "Given Names: ",
        "Gender": "Gender: ",
        "Date of Birth": "Date of Birth: ",
        "Place of Birth": "Place of Birth: ",
        "Issued On": "Issued On: ",
        "Expires On": "Expires On: "
    }
    
    formatted_info = {}
    for key, prefix in fields.items():
        start_index = extracted_text.find(prefix)
        if start_index != -1:
            end_index = extracted_text.find("\n", start_index)
            value = extracted_text[start_index + len(prefix):end_index].strip()
            if key not in formatted_info:  # Ensure no duplicates
                formatted_info[key] = value

    formatted_text = "\n".join([f"{key}: {value}" for key, value in formatted_info.items()])
    return formatted_text

if __name__ == "__main__":
    image_path = './media/passport-card-sample.jpg'
    print(extract_information_from_image(image_path))
