import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# Load dataset
file_path = "kabaddi_data.csv"  # Ensure this path is correct
data = pd.read_csv(file_path)

# Load encoders
team1_encoder = joblib.load("Team 1_encoder.pkl")
team2_encoder = joblib.load("Team 2_encoder.pkl")
outcome_encoder = joblib.load("Outcome_encoder.pkl")

# Encode categorical columns
data["Team 1"] = team1_encoder.transform(data["Team 1"])
data["Team 2"] = team2_encoder.transform(data["Team 2"])
data["Outcome"] = outcome_encoder.transform(data["Outcome"])

# Split data into features and target
X = data.drop(columns=["Outcome"])
y = data["Outcome"]

# Flatten y to be 1D (avoid warning)
y = y.values.ravel()  # Using ravel() to ensure y is a 1D array

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the base model
base_model = RandomForestClassifier(n_estimators=100, random_state=42)
base_model.fit(X_train, y_train)

# Calibrate the model
calibrated_model = CalibratedClassifierCV(base_model, method="sigmoid", cv="prefit")
calibrated_model.fit(X_train, y_train)

# Evaluate the calibrated model
y_pred = calibrated_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Calibrated Model Accuracy: {accuracy:.2f}")

# Save the calibrated model
joblib.dump(calibrated_model, "calibrated_kabaddi_model.pkl")
print("Calibrated model saved as 'calibrated_kabaddi_model.pkl'")
