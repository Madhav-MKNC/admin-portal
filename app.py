#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from werkzeug.utils import secure_filename

from utils import *
from functools import wraps

import os
from dotenv import load_dotenv
load_dotenv()


# Initialzing flask app
app = Flask(__name__)

# secret key
# app.secret_key = os.getenv("FLASK_SECRET_KEY")  # Change this to a strong random key in a production environment
app.secret_key = str(unique_id()).replace("-","")

# URL to the chatbot
CHATBOT_URL = "http://localhost:8081"
print(f"\n[+] Chatbot URL is: {CHATBOT_URL}\n")


# only logged in access
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('authenticated'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function



# Routes below:
"""
/           => index
/login      => admin login page
/dashboard  => admin dashboard
/upload     => for uploading files
/delete     => for deleting a uploaded file
/chatbot    => redirect to chatbot
/logout     => admin logout
"""

# index
@app.route('/')
def index():
    return render_template('index.html')

# login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if is_authenticated(username, password):
            # Save the authenticated status in the session
            session['authenticated'] = True
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid credentials. Please try again.'
            return render_template('login.html', error=error)
    return render_template('login.html')

# dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    # Check if the user is authenticated in the session
    if not session.get('authenticated'):
        return redirect(url_for('login'))

    files = os.listdir(UPLOAD_FOLDER)
    return render_template('dashboard.html', files=files)

# uploaded files here
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    # Serve the uploaded file directly from the server
    return send_from_directory(UPLOAD_FOLDER, filename)

# upload
@app.route('/upload', methods=['POST'])
@login_required
def upload():
    if request.method == 'POST':
        files = request.files.getlist('file')  # Get a list of uploaded files
        
        if not files:
            flash('No files selected')
            return redirect(url_for('dashboard'))

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
            else:
                flash('Invalid file type')
                return redirect(url_for('dashboard'))

        flash('Files uploaded successfully')
        return redirect(url_for('dashboard'))

# delete an uploaded file  
@app.route('/delete/<filename>')
@login_required
def delete(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        flash('File deleted successfully')
    else:
        flash('File not found')
    return redirect(url_for('dashboard'))

# upload files from google drive
@app.route('/upload_google_drive', methods=['POST'])
@login_required
def upload_google_drive():
    # Here, you would implement the logic to handle the Google Drive file upload.
    # Since implementing the Google Drive integration requires OAuth 2.0 authentication and API integration,
    # it goes beyond the scope of a simple file upload example.

    # You can use the Google Drive API or a Google Drive SDK to integrate the functionality.
    # It involves obtaining authorization, accessing the user's Google Drive, and uploading the file.

    # For the sake of this example, we'll just display a message indicating the feature is not implemented.
    flash('Google Drive upload feature is not implemented yet.')
    return redirect(url_for('dashboard'))


# To handle URL submission
@app.route('/handle_url', methods=['POST'])
@login_required
def handle_url():
    if request.method == 'POST':
        url = request.form.get('url')
        result_message = handle_urls(url)
        flash(result_message)
    return redirect(url_for('dashboard'))

# chatbot
@app.route('/chatbot')
def chatbot_redirect():
    if not valid_url(CHATBOT_URL):
        error = f'Unable to reach chatbot url = {CHATBOT_URL}'
        flash(error)
        return render_template('index.html')
    return redirect(CHATBOT_URL)

# logout
@app.route('/logout')
def logout():
    # Clear the authenticated status from the session
    session.pop('authenticated', None)
    return redirect(url_for('login'))


# run server
def start_server():
    app.run(host="0.0.0.0", port=80, debug=True)


if __name__ == '__main__':
    start_server()
