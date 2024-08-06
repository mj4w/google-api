import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import io
from googleapiclient.errors import HttpError
import os
from dotenv import load_dotenv

load_dotenv()

"""
Service Account Credentials
https://console.cloud.google.com/apis/credentials?project=nice-carving-431716-b4

1. Create Credentials / Service Account
2. Edit Service Account / Go to Keys
3. Add Key / Create New Key.json
"""

scope = ['https://www.googleapis.com/auth/drive']
service_account_json_key = '../nice-carving-431716-b4-0cb91488cbe4.json'
credentials = service_account.Credentials.from_service_account_file(
    filename=service_account_json_key, 
    scopes=scope)
service = build('drive', 'v3', credentials=credentials)

folder_id = '1wjRKZFbvoFLPBjdwqsd4zIi7nYevNsds'
file_names = ['new_candidates_by_source_07-24-2024.xlsx', 'Screenshot 2024-07-22 135818.png']
# file types https://mimetype.io/all-types
mime_types = ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet','image/png']

for file_name,mime_type in zip(file_names, mime_types):
    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }
    media = MediaFileUpload('./assets/{0}'.format(file_name), mimetype=mime_type)

    try:
        service.files().create(
            body=file_metadata,
            media_body=media,
            fields = 'id'
        ).execute()
        print(f'Uploading file successfully')
    except HttpError as error:
        print(f'An error occurred: {error}')
    
    