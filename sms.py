import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
import joblib  # Library to save the model

# Load your dataset
sms = pd.read_csv('/csv/spam.csv', encoding='ISO-8859-1')

# Data cleaning
cols_to_drop = ['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4']
sms.drop(cols_to_drop, axis=1, inplace=True)
sms.columns = ['label', 'message']
sms['label'] = sms['label'].replace('ham', 'legit')
# Initialize the CountVectorizer and fit it
cv = CountVectorizer(decode_error='ignore')
X = cv.fit_transform(sms['message'])

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, sms['label'], test_size=0.3, random_state=101)

# Initialize and train the Multinomial Naive Bayes model
mnb = MultinomialNB()
mnb.fit(X_train, y_train)

# Save the trained model and CountVectorizer
joblib.dump(mnb, 'spam_detector_model.pkl')  # Saves the model
joblib.dump(cv, 'cv_vectorizer.pkl')  # Saves the CountVectorizer

print("Model and CountVectorizer have been saved successfully.")
