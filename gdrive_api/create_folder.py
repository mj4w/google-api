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

"""
Share user function:
To create and share the folder to your personal email
"""

def share_with_user(service, file_id, user_email):
    user_permission = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': user_email
    }
    try:
        service.permissions().create(
            fileId=file_id,
            body=user_permission,
            fields='id',
        ).execute()
        print(f'Shared file {file_id} with {user_email}')
    except HttpError as error:
        print(f'An error occurred: {error}')

folders = ['drive1', 'drive2'] # the folder that to be created
folder_ids = {}
account_email = os.getenv('PERSONAL_EMAIL')


for folder in folders:
    file_metadata = {
        'name': folder,
        'mimeType': 'application/vnd.google-apps.folder', # mimeType https://developers.google.com/drive/api/guides/mime-types
    }
    
    folder_response = service.files().create(body=file_metadata, fields='id').execute()
    folder_id = folder_response.get('id')
    folder_ids[folder] = folder_id
    print(f'Created folder {folder} with ID {folder_id}')

    share_with_user(service, folder_id, account_email)

"""
Create file in each folder
"""
for folder_name, folder_id in folder_ids.items():
    file_metadata = {
        'name': 'example.txt',
        'parents': [folder_id]
    }
    media = MediaFileUpload('example.txt', mimetype='text/plain')
    
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    file_id = file.get('id')
    print(f'Created file example.txt in folder {folder_name} with ID {file_id}')

    share_with_user(service, file_id, account_email)
