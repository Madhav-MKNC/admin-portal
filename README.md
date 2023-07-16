# Chat Bot Web Application

The Chat Bot Web Application is a web-based interactive chatbot that utilizes Large Language Models (LLMs) and Langchain technology to interact with documents and data managed on the Admin Dashboard. This application allows users to have natural language conversations with the chatbot, making it a powerful tool for retrieving information, answering questions, and assisting users with various tasks.

## Features

- Natural Language Interaction: The chatbot uses state-of-the-art Large Language Models (LLMs) to understand and respond to user queries in a human-like manner.
- Seamless Integration: The chatbot is seamlessly integrated with the Admin Dashboard, enabling access to documents and data managed by the administrator.
- Interactive Communication: Users can have real-time interactive conversations with the chatbot, making it a user-friendly and engaging experience.
- Advanced Search: The chatbot utilizes Langchain technology to perform advanced searches across documents, ensuring accurate and relevant responses to user queries.
- User-Friendly Interface: The web application offers an intuitive and user-friendly interface, making it accessible to users with varying levels of technical expertise.

## Getting Started

To set up and run the Chat Bot Web Application, follow these steps:

1. **Clone the Repository**: Clone this repository to your local machine.

2. **Install Dependencies**: Ensure you have Python and the required libraries installed. Use the following command to install the necessary dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set Environment Variables**: Create a `.env` file and set the following environment variables:

   ```plaintext
   FLASK_SECRET_KEY=your_secret_key_here
   ```

   Replace `your_secret_key_here` with a strong random key for Flask session management.

4. **Load Admin Users**: Prepare an `users.json` file containing the admin user data, and place it in the root directory of the application. The JSON file should have the following format:

   ```json
   [
       {
           "username": "user1",
           "password": "password1"
       },
       {
           "username": "user1",
           "password": "password2"
       },
       // Add more users as needed
   ]
   ```

   Make sure to replace `user1`, `user2`, etc., with actual usernames, and `password1`, `password2`, etc., with the passwords of the respective users.

5. **Start the Application**: Run the Flask application using the following command:

   ```bash
   python app.py
   ```

   The application will be accessible at `http://localhost:8081`.

## Usage

**Chatbot Interaction**: To use the Chat Bot Web Application, go to `http://localhost:8081/chat`. Start interacting with the chatbot by typing your queries in natural language.

## License

This project is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute it as per the terms of the license.

---
*Note: Replace `http://localhost:8081` with the actual deployment URL if the application is hosted on a remote server.*
