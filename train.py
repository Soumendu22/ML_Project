import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib  # To save the model

# Load the dataset
data = pd.read_csv('UPI.csv')

# Display the first few rows of the dataset (optional)
print(data.head())

# Rename columns if necessary (adjust based on the dataset structure)
# data.columns = ["column1", "column2", ...]  # Adjust accordingly

# Feature columns and target
X = data.drop(columns=['fraud'])  # Use all columns except the target
y = data['fraud']  # Assuming 'fraud' is the target column (1 for fraud, 0 for non-fraud)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Initialize and train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluate the model
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Save the trained model to a file
joblib.dump(model, 'online_payments_fraud_model.pkl')
