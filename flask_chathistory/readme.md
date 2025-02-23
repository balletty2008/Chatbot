# Chatbot App with Registration, Login, and Chat History

This  chatbot application allows users to register, log in, interact with a bot, and view their chat history. The application uses Flask, SQLAlchemy for database management, and Flask-Bcrypt for password hashing.

## Features

- **User Registration**: Users can create an account with a unique username and password.
- **Login**: Registered users can log in to access the chatbot.
- **Chat Interaction**: Users can interact with the chatbot, which stores their messages and bot responses.
- **Chat History**: Users can view their past chats with the bot.
- **Logout**: Users can log out and clear their session.

## Installation Instructions

1. **Clone the repository (or download the project files):**
    ```bash
    git clone https://github.com/chatbot.git
    cd chatbot
    ```

2. **Set up a virtual environment:**
   It's recommended to use a virtual environment to avoid any conflicts with other Python packages.

    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment:**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install required packages:**
    - Install the necessary Python libraries using `pip`:
    - pip install Flask Flask-SQLAlchemy
    - pip install Flask-Bcrypt


    ```bash
    pip install -r requirements.txt
    ```

5. **Create the SQLite Database:**
    Once the application is set up, the app will automatically create the `chatbot.db` SQLite database when it runs for the first time. Ensure that the app has access to the folder where the database file will be created.

6. **Run the Flask App:**
    You can start the Flask application with the following command:

    ```bash
    python app.py
    ```

7. **Access the App:**
    The application will run at `http://127.0.0.1:5000/`. You can now open the URL in your browser to register, log in, and interact with the chatbot.

## Folder Structure

### Template Files:

- **`login.html`**: User login form.
- **`register.html`**: User registration form.
- **`chat.html`**: Chat interface for users to interact with the bot.
- **`chat_history.html`**: Displays the chat history of the logged-in user.

## Requirements

- Python (ensure Python is installed)
- Flask
- Flask-SQLAlchemy
- Flask-Bcrypt