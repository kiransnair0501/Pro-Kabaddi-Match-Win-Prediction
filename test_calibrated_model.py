import pandas as pd
import joblib
import numpy as np

# Load calibrated model and encoders
model = joblib.load("calibrated_kabaddi_model.pkl")
team1_encoder = joblib.load("Team 1_encoder.pkl")
team2_encoder = joblib.load("Team 2_encoder.pkl")
outcome_encoder = joblib.load("Outcome_encoder.pkl")

# Test data
test_input = {
    "Team 1": ["U Mumba"],
    "Team 2": ["Puneri Paltan"],
    "Time Left": [5],
    "Team 1 Score": [20],
    "Team 2 Score": [5],
    "Raid Success Rate 1": [0.45],
    "Raid Success Rate 2": [0.10],
    "Tackle Success Rate 1": [0.60],
    "Tackle Success Rate 2": [0.0]
}

# Prepare test DataFrame
test_df = pd.DataFrame(test_input)
test_df["Team 1"] = team1_encoder.transform(test_df["Team 1"])
test_df["Team 2"] = team2_encoder.transform(test_df["Team 2"])

# Get probabilities for all classes (Team 1 Wins, Team 2 Wins, Draw)
probabilities = model.predict_proba(test_df)[0]

# Get the index of the class with the highest probability
max_index = np.argmax(probabilities)

# Decode the predicted outcome using the highest probability's index
predicted_outcome = outcome_encoder.classes_[max_index]

# Print the predicted outcome and the corresponding probabilities
print(f"Predicted Outcome: {predicted_outcome}")
print(f"Winning Chances:")
print(f"Team 1: {probabilities[0] * 100:.2f}%")
print(f"Team 2: {probabilities[1] * 100:.2f}%")
print(f"Draw: {probabilities[2] * 100:.2f}%")
