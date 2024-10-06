from flask import Flask, request, redirect, url_for, render_template, session, flash, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import joblib
import pandas as pd

app = Flask(__name__)
app.secret_key = 'soumendu'  # Set a secret key for session management
# model = joblib.load('online_payments_fraud_model.pkl')

# Connect to SQLite3
def get_db_connection():
    conn = sqlite3.connect('database.db')  # Create a new SQLite3 database file
    conn.row_factory = sqlite3.Row  # To return rows as dictionaries
    return conn

# Create table if not exists
def create_table():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()

# Call create_table when the app starts
create_table()

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
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            
            # Check if email already exists
            cur.execute('SELECT * FROM user WHERE email = ?', (email,))
            existing_user = cur.fetchone()
            
            if existing_user:
                conn.close()
                return redirect(url_for('landing', message='Email already registered', category='warning'))

            # Hash the password
            hashed_password = generate_password_hash(password, method='sha256')
            
            # Insert data into SQLite3
            cur.execute('INSERT INTO user (name, email, password) VALUES (?, ?, ?)', 
                        (name, email, hashed_password))
            conn.commit()  # Ensure the transaction is committed
            conn.close()

            session['user_name'] = name  # Store user name in session
            return jsonify({'status': 'success', 'message': 'Registration successful', 'category': 'success'})

        except sqlite3.Error as e:
            # Log the error and return a meaningful message
            print(f"SQLite error: {e}")
            return jsonify({'status': 'error', 'message': 'Database error occurred', 'category': 'danger'})
    else:
        return redirect(url_for('landing', message='Please fill in all fields', category='danger'))

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    if email and password:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute('SELECT * FROM user WHERE email = ?', (email,))
        user = cur.fetchone()
        conn.close()

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

@app.route('/fraud_type', methods=['POST'])
def fraud_type():
    fraud_type = request.form.get('fraud_type')

    # Redirect user based on the selected fraud type
    if fraud_type == 'UPI':
        return redirect(url_for('upi_fraud'))
    elif fraud_type == 'bank_transaction':
        return redirect(url_for('bank_transaction_fraud'))
    elif fraud_type == 'email':
        return redirect(url_for('email'))
    elif fraud_type == 'sms_fraud':
        return redirect(url_for('sms_fraud'))
    else:
        return redirect(url_for('home'))

model = joblib.load('spam_detector_model.pkl')  # Replace with your model path
cv = joblib.load('cv_vectorizer.pkl')  # Replace with your vectorizer path
@app.route('/sms_fraud', methods=['GET', 'POST'])
def sms():
    if request.method == 'POST':
        message = request.form.get('message')
        if message:
            transformed_message = cv.transform([message])
            prediction = model.predict(transformed_message)

            if prediction[0] == 'spam':
                return render_template('sms_fraud.html', prediction='Spam', message=message)
            else:
                return render_template('sms_fraud.html', prediction='Not Spam', message=message)

    return render_template('sms_fraud.html')

# Load your trained model and vectorizer
modelemail = joblib.load('email_detector_model.pkl')  # Replace with your model path
cvemail = joblib.load('cv_vectorizer_email.pkl')  # Replace with your vectorizer path

@app.route('/email', methods=['GET', 'POST'])
def email():
    if request.method == 'POST':
        email_text = request.form.get('email_text')
        if email_text:
            # Transform the input email text using the loaded vectorizer
            transformed_email = cvemail.transform([email_text])
            prediction = modelemail.predict(transformed_email)

            # Render the result in the HTML template
            if prediction[0] == 'Phishing Email':
                return render_template('email_fraud.html', prediction='Phishing', email=email_text)
            else:
                return render_template('email_fraud.html', prediction='Not Phishing', email=email_text)

    return render_template('email_fraud.html')


# Define routes for each type of fraud page
@app.route('/upi_fraud')
def upi_fraud():
    return render_template('UPI.html')

@app.route('/bank_transaction_fraud')
def bank_transaction_fraud():
    return render_template('bank_transaction.html')

@app.route('/sms_fraud')
def sms_fraud():
    return render_template('sms_fraud.html')

# @app.route('/predict', methods=['POST'])
# def predict():
#     # Get user input from the form
#     amount = request.form.get('amount')
#     transaction_time = request.form.get('transaction_time')
#     # Add additional fields as necessary

#     # Prepare input for prediction
#     input_data = pd.DataFrame([[amount, transaction_time]], columns=['amount', 'transaction_time'])  # Adjust according to your feature set
#     prediction = model.predict(input_data)

#     if prediction[0] == 1:
#         return "Fraud detected!"
#     else:
#         return "Transaction is safe."

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_name', None)  # Clear the session
    return redirect(url_for('landing', message='Logged out successful', category='success'))

if __name__ == '__main__':
    app.run(debug=True)
