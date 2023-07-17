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

1. `app.py`: The main Flask application file containing the server logic.
2. `admin_users.json`: A JSON file containing a list of admin users' credentials.
3. `uploads/`: A folder to store the uploaded files.

## Installation and Setup
1. Clone the repository from GitHub.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Set the environment variable `FLASK_SECRET_KEY` to a strong random key for session management and security. **Note:** In a production environment, ensure this key is kept secret and not hard-coded.
4. Ensure the `admin_users.json` file contains valid admin user credentials.

## How to Run
To start the Flask server, run the `start_server()` function in the `app.py` file. The server will run on `http://0.0.0.0:80/` and listen to incoming requests.

```bash
python app.py
```

## Routes
The Flask application exposes the following routes:

1. `/`: The homepage of the Admin Portal.
2. `/login`: The login page for administrators to authenticate themselves.
3. `/dashboard`: The main dashboard page where administrators can see the uploaded files and manage them.
4. `/uploads/<filename>`: A route to serve uploaded files directly from the server.
5. `/upload`: A route to upload files to the server.
6. `/delete/<filename>`: A route to delete uploaded files from the server.
7. `/logout`: A route to log out and clear the authenticated session.
8. `/chatbot`: Redirect to chatbot.

## Important Notes
1. The project uses Flask's built-in session management to store the authenticated status, which is not suitable for production environments. In a real-world application, consider using a more robust session management solution.
2. The `allowed_file()` function allows only specific file types (txt, pdf, doc, docx, csv) to be uploaded. Modify the `ALLOWED_EXTENSIONS` set to include additional file types if required.
3. In a production environment, it's crucial to ensure secure file uploads to prevent any potential security risks.

## License
This project is licensed under the [MIT License](LICENSE). Feel free to use and modify it according to your needs.