import pathlib
import textwrap
import os
from dotenv import load_dotenv
import PIL.Image
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import json
import uuid
import re

load_dotenv()

def extract_information_from_image(image_path):
    """
    Extracts information from a passport image using Gemini AI.

    Parameters:
    - image_path (str): Path to the input image file.

    Returns:
    - dict: Extracted information in structured JSON format.
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
    prompt = """
    Extract the following information from this passport image:
    - Passport Number: 
    - Nationality: 
    - Surname: 
    - Given Names: 
    - Gender: 
    - Date of Birth: 
    - Place of Birth: (or Place of Origin)
    - Issued On: 
    - Expires On: 
    If the information is labeled differently in the passport, standardize it to the above fields.
    """
    response = model.generate_content([prompt, img], safety_settings=safety_settings)

    # Extract and format the text information
    extracted_text = response.text.strip()
    formatted_info = format_passport_information(extracted_text)

    # Generate a unique filename with UUID
    special_id = str(uuid.uuid4())
    filename = f'passport_{special_id}.json'

    # Save the formatted information to a JSON file
    # save_to_json(formatted_info, f'./Information/{filename}')

    return formatted_info

def format_passport_information(extracted_text):
    """
    Formats the extracted information into a structured JSON format.

    Parameters:
    - extracted_text (str): The raw extracted text.

    Returns:
    - dict: The formatted information as a structured JSON.
    """
    fields = {
        "Passport Number": r"Passport Number: (.+)",
        "Nationality": r"Nationality: (.+)",
        "Surname": r"Surname: (.+)",
        "Given Names": r"Given Names: (.+)",
        "Gender": r"Gender: (.+)",
        "Date of Birth": r"Date of Birth: (.+)",
        "Place of Birth": r"Place of Birth: (.+)|Place of Origin: (.+)",
        "Issued On": r"Issued On: (.+)",
        "Expires On": r"Expires On: (.+)"
    }
    
    formatted_info = {}
    for key, pattern in fields.items():
        match = re.search(pattern, extracted_text)
        if match:
            # Handle multiple groups in regex (e.g., Place of Birth / Place of Origin)
            formatted_info[key] = match.group(1).strip() if match.group(1) else match.group(2).strip()

    return formatted_info

# def save_to_json(data, file_path):
#     """
#     Saves the given data to a JSON file.

#     Parameters:
#     - data (dict): The data to save.
#     - file_path (str): The path to the JSON file.
#     """
#     os.makedirs(os.path.dirname(file_path), exist_ok=True)
#     with open(file_path, 'w', encoding='utf-8') as json_file:
#         json.dump(data, json_file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    image_path = './media/page_1.jpg'
    extracted_info = extract_information_from_image(image_path)
    print(json.dumps(extracted_info, indent=4))
