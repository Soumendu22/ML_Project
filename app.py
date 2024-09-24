from flask import Flask, request, redirect, url_for, render_template, session, flash, jsonify
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'soumendu'  # Set a secret key for session management

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['ML']
user_collection = db['user']

@app.route('/')
def landing():
    session.pop('user_name', None)  # Clear session if the user is at the index page
    return render_template('landing.html')

@app.route('/signup', methods=['POST'])
def signup():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    if name and email and password:
        # Check if email already exists
        existing_user = user_collection.find_one({'email': email})
        if existing_user:
            return redirect(url_for('landing', message='Email already registered', category='warning'))

        # Hash the password
        hashed_password = generate_password_hash(password, method='sha256')
        # Insert data into MongoDB
        user_collection.insert_one({
            'name': name,
            'email': email,
            'password': hashed_password
        })
        session['user_name'] = name  # Store user name in session
        return jsonify({'status': 'success', 'message': 'Registration successful', 'category': 'success'})
    else:
        return redirect(url_for('landing', message='Please fill in all fields', category='danger'))

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    if email and password:
        user = user_collection.find_one({'email': email})
        if user and check_password_hash(user['password'], password):
            session['user_name'] = user['name']  # Store user name in session
            return redirect(url_for('home', message='Login successful', category='success'))
        else:
            return redirect(url_for('landing', message='Invalid credentials', category='danger'))
    else:
        return redirect(url_for('landing', message='Please fill in both fields', category='danger'))

@app.route('/main')
def home():
    name = session.get('user_name')  # Retrieve user name from session

    if name is None:
        # Redirect to index if user is not signed in
        return redirect(url_for('landing'))

    # Render the main page with the user's name
    return render_template('main.html', user_name=name)

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_name', None)  # Clear the session
    return redirect(url_for('landing', message='Logged out successful', category='success'))

if __name__ == '__main__':
    app.run(debug=True)
