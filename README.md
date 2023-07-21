# admin-portal
Admin dashboard for managing data for AI-chatbot


# Project Development Details

## Project Description
This project is an Admin Portal for managing data for an AI chatbot. It allows administrators to log in, upload, and delete files. The application is built using Flask, a popular Python web framework, and it provides a simple web interface to interact with the chatbot's data.

## Prerequisites
Before running the application, ensure the following prerequisites are met:

1. Python 3.x is installed on the system.
2. Required Python packages are installed. You can install them using `pip install -r requirements.txt`.
3. The environment variables `FLASK_SECRET_KEY` and any other required variables should be set.

## Project Structure
The project consists of the following files:

0. `main.py`: The man program script. Starting point.
1. `app.py`: The main Flask application file containing the server logic.
2. `admin_users.json`: A JSON file containing a list of admin users' credentials.
3. `client_secret.json`: A JSON file containing Google Drive API keys and credentials. (Get it from here [https://console.cloud.google.com/])
4. `.stored_files.json`: A JSON file used for attaining Data transparency, this file is kept in synced with the pinecone vector database. (maintained by the `manage_vectordb.py`)
5. `utils.py`: Utilites / helper functions for `app.py`
6. `manage_vectordb.py`: Module for managing the data on Pinecone vector database. Also a standalone script for testing the database.

## Installation and Setup
1. Clone the repository from GitHub.

```(bash)
git clone https://github.com/madhav-mknc/admin-portal
cd https://github.com/madhav-mknc/admin-portal
```
2. Install the required dependencies using:
```(bash)
pip install -r requirements.txt
```
3. Set the environment variable `FLASK_SECRET_KEY` to a strong random key for session management and security. **Note:** In a production environment, ensure this key is kept secret and not hard-coded.
4. Ensure the `admin_users.json` file contains valid admin user credentials.
5. Set all the required env variables mentioned in ".env" file.

## How to Run
- To start the Flask server, run the `start_server()` function in the `app.py` file. The server will run on `http://0.0.0.0:80/` and listen to incoming requests.

```bash
python app.py
```
or 
```bash
python main.py
```

- For testing QnA: Open another command line in the same directory and follow the following commands:
```(bash)
python manage_vectordb.py
```

    * ".stats" is a command short for index.describe_index_stats()
    * ".reset_index" is for resetting the index by deleting and creating a new one.

## Routes
The Flask application exposes the following routes:

1. `/`: The homepage of the Admin Portal.
2. `/login`: The login page for administrators to authenticate themselves.
3. `/dashboard`: The main dashboard page where administrators can see the uploaded files and manage them.
4. `/uploads/<filename>`: A route to serve uploaded files directly from the server.
5. `/upload`: A route to upload files to the server.
6. `/upload_google_drive`: A route for uploading files from Google Drive.
7. `/handle_url`: A route for fetching data using a URL.
6. `/delete/<filename>`: A route to delete uploaded files from the server.
7. `/logout`: A route to log out and clear the authenticated session.
8. `/chatbot`: Redirect to chatbot.

## Important Notes
1. The project uses Flask's built-in session management to store the authenticated status, which is not suitable for production environments. In a real-world application, consider using a more robust session management solution.
2. The `allowed_file()` function allows only specific file types (txt, pdf, doc, docx, csv) to be uploaded. Modify the `ALLOWED_EXTENSIONS` set to include additional file types if required.
3. In a production environment, it's crucial to ensure secure file uploads to prevent any potential security risks.

## License
This project is licensed under the [MIT License](LICENSE). Feel free to use and modify it according to your needs.