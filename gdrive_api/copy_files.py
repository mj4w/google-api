import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
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


source_file_id = '1vRhIYVAzB8mzWv5zOnbe3cZhVnMR6Rvd'
folder_ids = ['1wjRKZFbvoFLPBjdwqsd4zIi7nYevNsds']


"""
File is linked in all parents folder
"""
# file_metadata = {
#     'name': 'Image',
#     'parents': folder_ids,
#     'starred': True,
#     'description': 'Sample Description'
# }
# service.files().copy(
#     fileId = source_file_id,
#     body = file_metadata
# ).execute()

"""
File is treated as individual entity
"""

for folder_id in folder_ids:
    file_metadata = {
        'name': 'Image',
        'parents': [folder_id],
        'starred': True,
        'description': 'Sample Description'
    }   
    service.files().copy(
        fileId = source_file_id,
        body = file_metadata
    ).execute()