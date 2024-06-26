import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def upload_pdf(file_path):
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("No API key found. Please set the API_KEY environment variable in the .env file.")

    files = [
        ('file', ('file', open(file_path, 'rb'), 'application/octet-stream'))
    ]
    headers = {
        'x-api-key': api_key
    }

    response = requests.post(
        'https://api.chatpdf.com/v1/sources/add-file', headers=headers, files=files)

    if response.status_code == 200:
        return response.json()['sourceId']
    else:
        print('Status:', response.status_code)
        print('Error:', response.text)
        return None


def chat_with_pdf(source_id, user_message):
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("No API key found. Please set the API_KEY environment variable in the .env file.")

    headers = {
        'x-api-key': api_key,
        "Content-Type": "application/json",
    }

    data = {
        'sourceId': source_id,
        'messages': [
            {
                'role': "user",
                'content': user_message,
            }
        ]
    }

    response = requests.post(
        'https://api.chatpdf.com/v1/chats/message', headers=headers, json=data)

    if response.status_code == 200:
        return response.json()['content']
    else:
        print('Status:', response.status_code)
        print('Error:', response.text)
        return None

# Main workflow
file_path = 'Pakistan_Constitution.pdf'
source_id = upload_pdf(file_path)

if source_id:
    print('Source ID:', source_id)
    user_message = input("What is your query about the Pakistani Constitution?\n")
    answer = chat_with_pdf(source_id, user_message)
    if answer:
        print('Answer:', answer)
