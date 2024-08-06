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

file_ids = ['1vRhIYVAzB8mzWv5zOnbe3cZhVnMR6Rvd','1TUo3d9Dkq24NEhf4YVSiicNZZGA5tYTL']
file_names = ['test2.png','test.xlsx']

for file_id, file_name in zip(file_ids, file_names):
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fd=fh,request=request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f'Download progress {0}'.format(status.progress() * 100))
    fh.seek(0)
    
    with open(os.path.join('./assets', file_name), 'wb') as f:
        f.write(fh.read())
        f.close()