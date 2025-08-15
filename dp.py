import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV
import pickle

# Load dataset
data = pd.read_csv("kabaddi_data.csv")

# Features and target
X = data.drop(columns=["Outcome"])  # Drop the target column
y = data["Outcome"]

# Define consistent feature names (update based on your dataset)
feature_names = [
    "Team 1", "Team 2", "Time Left",
    "Raid Success Rate 1", "Raid Success Rate 2",
    "Tackle Success Rate 1", "Tackle Success Rate 2",
    "Team 1 Home", "Team 2 Home"
]
X.columns = feature_names  # Ensure feature names match

# Encode categorical columns (if any)
label_encoders = {}
for col in X.select_dtypes(include=['object']).columns:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col])
    label_encoders[col] = le

y_encoder = LabelEncoder()
y = y_encoder.fit_transform(y)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Feature scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Calibrate the model
calibrated_model = CalibratedClassifierCV(model, method="sigmoid", cv="prefit")
calibrated_model.fit(X_test_scaled, y_test)

# Save the model, scaler, and encoders
with open("kabaddi_calibrated_model.pkl", "wb") as model_file:
    pickle.dump(calibrated_model, model_file)
with open("scaler.pkl", "wb") as scaler_file:
    pickle.dump(scaler, scaler_file)
with open("encoders.pkl", "wb") as encoders_file:
    pickle.dump({"Outcome": y_encoder, **label_encoders}, encoders_file)

print("Model Accuracy: {:.2f}".format(model.score(X_test_scaled, y_test)))
print("Model, scaler, and encoders saved successfully.")
