import joblib

# Load the encoders
team1_encoder = joblib.load("Team 1_encoder.pkl")
team2_encoder = joblib.load("Team 2_encoder.pkl")
outcome_encoder = joblib.load("Outcome_encoder.pkl")

print("Team 1 Encoder Classes:", team1_encoder.classes_)
print("Team 2 Encoder Classes:", team2_encoder.classes_)
print("Outcome Encoder Classes:", outcome_encoder.classes_)
