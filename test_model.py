import pickle
import pandas as pd

# Load the saved model, scaler, and encoders
with open("kabaddi_calibrated_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)
with open("scaler.pkl", "rb") as scaler_file:
    scaler = pickle.load(scaler_file)
with open("encoders.pkl", "rb") as encoders_file:
    encoders = pickle.load(encoders_file)

# Define consistent feature names
feature_names = [
    "Team 1", "Team 2", "Time Left",
    "Raid Success Rate 1", "Raid Success Rate 2",
    "Tackle Success Rate 1", "Tackle Success Rate 2",
    "Team 1 Home", "Team 2 Home"
]

# Function for predicting outcomes
def predict_outcome(input_data):
    # Ensure input matches expected feature format
    input_data_full = {feature: 0 for feature in feature_names}  # Default all features to 0

    # Map input values to the correct features
    for i, feature in enumerate(feature_names[:len(input_data)]):  # Map only provided values
        input_data_full[feature] = input_data[i]

    # Convert to DataFrame and scale
    input_df = pd.DataFrame([input_data_full])
    input_data_scaled = scaler.transform(input_df)

    # Predict probabilities
    probabilities = model.predict_proba(input_data_scaled)

    # Align probabilities with class labels
    y_encoder = encoders["Outcome"]
    class_probabilities = dict(zip(y_encoder.classes_, probabilities[0]))

    # Sort by highest probability
    sorted_classes = sorted(class_probabilities.items(), key=lambda x: x[1], reverse=True)
    predicted_outcome = sorted_classes[0][0]

    print(f"Prediction: {predicted_outcome}")
    for cls, prob in sorted_classes:
        print(f"{cls}: {prob * 100:.2f}%")

    return predicted_outcome, class_probabilities

# Example input for testing (ensure it matches the feature format)
test_input = [1, 2, 3, 0.86, 0.84, 0.18, 0.71, 0, 0]  # Example input
predict_outcome(test_input)
