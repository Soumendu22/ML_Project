# detectemail.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
import joblib  # Library to save the model
import nltk
import re
from flask import Flask, request, jsonify

# Ensure you have the necessary NLTK resources
nltk.download('stopwords')

app = Flask(__name__)

# Function to clean text
def clean_text(text):
    if isinstance(text, str):  # Check if the input is a string
        text = text.lower()  # Convert to lowercase
        text = re.sub(r'\d+', '', text)  # Remove numbers
        text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
        return text
    return ''  # Return an empty string for NaN values or non-strings

# Load your dataset
file_path = 'csv/Phishing_Email.csv'
data = pd.read_csv(file_path)

# Data cleaning
data = data.dropna(subset=['Email Text'])  # Drop rows with NaN values
data['cleaned_text'] = data['Email Text'].apply(clean_text)  # Clean the email text

# Initialize the CountVectorizer and fit it
cv = CountVectorizer()
X = cv.fit_transform(data['cleaned_text'])

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, data['Email Type'], test_size=0.2, random_state=42)

# Initialize and train the Multinomial Naive Bayes model
mnb = MultinomialNB()
mnb.fit(X_train, y_train)

# Save the trained model and CountVectorizer
joblib.dump(mnb, 'email_detector_model.pkl')  # Saves the model
joblib.dump(cv, 'cv_vectorizer_email.pkl')  # Saves the CountVectorizer

print("Model and CountVectorizer have been saved successfully.")

# Load the model and vectorizer when the application starts
model = joblib.load('email_detector_model.pkl')
vectorizer = joblib.load('cv_vectorizer_email.pkl')

@app.route('/predict', methods=['POST'])
def predict_phishing_email():
    email_text = request.json.get('email_text', '')
    cleaned_text = clean_text(email_text)
    transformed_text = vectorizer.transform([cleaned_text])  # Use the loaded vectorizer
    prediction = model.predict(transformed_text)
    return jsonify({'prediction': prediction[0]})

if __name__ == "__main__":
    app.run(debug=True)
