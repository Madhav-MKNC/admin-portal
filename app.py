#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from werkzeug.utils import secure_filename

import json
import hashlib
from functools import wraps

import os
from dotenv import load_dotenv
load_dotenv()


# Initialzing flask app
app = Flask(__name__)

# secret key
app.secret_key = os.getenv("FLASK_SECRET_KEY")  # Change this to a strong random key in a production environment

# URL to the chatbot
CHATBOT_URL = "http://localhost:8081"
print(f"\n[+] Chatbot URL is: {CHATBOT_URL}\n")

# Folder to store uploaded files
app.config['UPLOAD_FOLDER'] = 'uploads'
if not os.path.exists('./uploads'):
    os.makedirs('uploads')

# Load admin users from the JSON file
ADMIN_USERS_FILE = 'admin_users.json'

def load_admin_users():
    admin_users = []
    if os.path.exists(ADMIN_USERS_FILE):
        with open(ADMIN_USERS_FILE, 'r') as file:
            admin_users = json.load(file)
    return admin_users

ADMIN_USERS = load_admin_users()


def is_authenticated(username, password):
    # Check if the provided username and password match any admin user
    for admin_user in ADMIN_USERS:
        if admin_user['username'] == username and hashlib.sha256(admin_user['password'].encode()).hexdigest() == hashlib.sha256(password.encode()).hexdigest():
            return True
    return False

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('authenticated'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def allowed_file(filename):
    # Check if the uploaded file has an allowed extension (customize this list as needed)
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




"""
Routes below:
/
/login
/dashboard
/upload
/delete
/logout
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

    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('dashboard.html', files=files)

# uploaded files here
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    # Serve the uploaded file directly from the server
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# upload
@app.route('/upload', methods=['POST'])
@login_required
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for('dashboard'))
        
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(url_for('dashboard'))
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File uploaded successfully')
            return redirect(url_for('dashboard'))
        
        else:
            flash('Invalid file type')
            return redirect(url_for('dashboard'))

@app.route('/delete/<filename>')
@login_required
def delete(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        flash('File deleted successfully')
    else:
        flash('File not found')
    return redirect(url_for('dashboard'))

# logout
@app.route('/logout')
def logout():
    # Clear the authenticated status from the session
    session.pop('authenticated', None)
    return redirect(url_for('login'))

# chatbot
@app.route('/chatbot')
def chatbot_redirect():
    return redirect(CHATBOT_URL)


# run server
def start_server():
    app.run(host="0.0.0.0", port=80, debug=True)


if __name__ == '__main__':
    start_server()
