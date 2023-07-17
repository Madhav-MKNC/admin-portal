# utilties / helper functions for app.py

import os
import json
import requests
import hashlib
from bs4 import BeautifulSoup
from uuid import uuid4 as unique_id

# directory for data storage
UPLOAD_FOLDER = "./uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Load admin users from the JSON file
ADMIN_USERS_FILE = 'admin_users.json'
ADMIN_USERS = []
if os.path.exists(ADMIN_USERS_FILE):
    with open(ADMIN_USERS_FILE, 'r') as file:
        ADMIN_USERS = json.load(file)

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

# for validating the url
def valid_url(url):
    try:
        response = requests.head(url)
        return response.status_code == 200
    except requests.RequestException:
        return False

# Function to handle URLs
def handle_urls(url):
    if not valid_url(url):
        return "Invalid URL"

    response = requests.get(url)
    file_name = str(unique_id()).replace("-","") + ".txt"
    save_path = os.path.join(UPLOAD_FOLDER, file_name)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        data_set = set()
        for text in soup.stripped_strings:
            if not text: continue
            data_set.add(text)
        with open(save_path, "w") as file:
            file.write("\n".join(list(data_set)))
        return "Data Fetched Successfully"
    else:
        return "Failed to Fetch Data"
    