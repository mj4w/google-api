import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
import io
from googleapiclient.errors import HttpError

scope = ['https://www.googleapis.com/auth/drive']
service_account_json_key = '../nice-carving-431716-b4-0cb91488cbe4.json'
credentials = service_account.Credentials.from_service_account_file(
    filename=service_account_json_key, 
    scopes=scope)
service = build('drive', 'v3', credentials=credentials)

def list_all_files(service):
    results = []
    page_token = None

    while True:
        try:
            param = {
                'pageSize': 1000,
                'fields': "nextPageToken, files(id, name, mimeType, size, modifiedTime)"
            }
            if page_token:
                param['pageToken'] = page_token

            response = service.files().list(**param).execute()
            items = response.get('files', [])
            results.extend(items)

            page_token = response.get('nextPageToken')
            if not page_token:
                break

        except HttpError as error:
            print(f'An error occurred: {error}')
            break

    return results

files = list_all_files(service)
for file in files:
    print(f"Name: {file['name']}, ID: {file['id']}, MimeType: {file.get('mimeType')}, Size: {file.get('size')}, Modified Time: {file.get('modifiedTime')}")
