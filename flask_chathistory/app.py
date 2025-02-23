from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image 
from flask import Flask, request, jsonify


# Load API key from .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("API key not found. Make sure it's set in the .env file.")

# Configure Gemini API
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

app = Flask(__name__)

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatbot.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Chat history model
class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_message = db.Column(db.String(200), nullable=False)
    bot_response = db.Column(db.String(500), nullable=False)

    user = db.relationship('User', back_populates="chats")

User.chats = db.relationship('ChatHistory', back_populates="user")

# Initialize database
with app.app_context():
    db.create_all()

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists. Please choose another.', 'danger')
            return redirect(url_for('register'))

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Login successful', 'success')
            return redirect(url_for('home'))
          ##  return redirect(url_for('chat'))

        flash('Invalid username or password', 'danger')

    return render_template('login.html')

# Home page
@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Prevent unauthorized access

    return render_template('home.html')  # Create a home.html page

# Chat page
@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    return render_template('chat.html')

# Chatbot API route for handling AJAX requests
@app.route('/chatbot', methods=['POST'])
def chatbot():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.json
    user_message = data.get("message")

    # Generate response using Gemini AI
    response = model.generate_content(user_message)
    bot_response = response.text

    # Save conversation to the database
    new_chat = ChatHistory(user_id=session['user_id'], user_message=user_message, bot_response=bot_response)
    db.session.add(new_chat)
    db.session.commit()

    return jsonify({"response": bot_response})

# Chat history page
@app.route('/chat_history')
def chat_history():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    history = ChatHistory.query.filter_by(user_id=session['user_id']).all()
    return render_template('chat_history.html', history=history)

@app.route("/image_upload", methods=["POST"])
def image_upload():
    if "image" not in request.files:
        return jsonify({"response": "No image provided"}), 400  # Handle missing image

    image = request.files["image"]

    if image.filename == "":
        return jsonify({"response": "No selected file"}), 400  # Handle empty filename

    # Process the image (Add your AI model or response here)
    return jsonify({"response": "Image received successfully!"})  # Debugging response

# Logout route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))


# Route to check database data
@app.route('/check_data')
def check_data():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    users = User.query.all()
    chats = ChatHistory.query.all()

    user_data = [{"id": user.id, "username": user.username} for user in users]
    chat_data = [{"user_id": chat.user_id, "user_message": chat.user_message, "bot_response": chat.bot_response} for chat in chats]

    return jsonify({"users": user_data, "chat_history": chat_data})


if __name__ == '__main__':
    app.run(debug=True)
