# utilties / helper functions for app.py

import os
import json
import hashlib
from uuid import uuid4 as unique_id

from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from manage_vectordb import add_file, delete_file, list_files


# Load admin users from the JSON file
ADMIN_USERS_FILE = 'admin_users.json'
ADMIN_USERS = []
if os.path.exists(ADMIN_USERS_FILE):
    with open(ADMIN_USERS_FILE, 'r') as file:
        ADMIN_USERS = json.load(file)
else:
    print(f"[error] {ADMIN_USERS_FILE} NOT FOUND")


# Check if the provided username and password match any admin user
def is_authenticated(username, password):
    for admin_user in ADMIN_USERS:
        if admin_user['username'] == username and hashlib.sha256(admin_user['password'].encode()).hexdigest() == hashlib.sha256(password.encode()).hexdigest():
            return True
    return False


# Check if the uploaded file has an allowed extension (customize this list as needed)
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx', 'csv'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# check if the parameter is a url
def is_url(filename):
    parsed_url = urlparse(filename)
    return parsed_url.scheme != '' and parsed_url.netloc != ''


# for validating the url
def valid_url(url):
    try:
        response = requests.head(
            url = url,
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        )
        return response.status_code == 200
    except requests.RequestException:
        return False

# Function to handle URLs
def handle_urls(url):
    if not valid_url(url):
        return "Invalid URL"

    upload_file_to_pinecone(file=url, isurl=True)
    return "Data Fetched Successfully"

# # Function to get Google Drive credentials using OAuth 2.0
# def get_google_drive_credentials():
#     # The scopes required for accessing Google Drive files
#     SCOPES = ['https://www.googleapis.com/auth/drive.file']
#     flow = InstalledAppFlow.from_client_secrets_file('client-secret.json', SCOPES)
#     credentials = flow.run_local_server(port=0)
#     return credentials

# # Function to upload file to Google Drive
# def upload_to_google_drive(file_path):
#     credentials = get_google_drive_credentials()
#     service = build('drive', 'v3', credentials=credentials)

#     file_metadata = {'name': os.path.basename(file_path)}
#     media = MediaFileUpload(file_path, resumable=True)

#     file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
#     return file.get('id')

# # Function to handle Google Drive authentication
# def authenticate_google_drive():
#     from google.oauth2.credentials import Credentials

#     # Load credentials from the session
#     creds = Credentials.from_authorized_user(session.get("credentials"), SCOPES)

#     # Build Google Drive service
#     drive_service = build("drive", "v3", credentials=creds)
#     return drive_service


# upload file to vector database storage (Pinecone)
def upload_file_to_pinecone(file, isurl=False):
    status = "ok"
    
    try:
        add_file(file, isurl=isurl)
    except Exception as e:
        status = e
    return status

# delete a file from pinecone (delete all the vectors related to)
def delete_file_from_pinecone(file):
    delete_file(file)


# get list of the source files stored on pinecone
def list_stored_files():
    return list_files()









