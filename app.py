from flask import Flask, render_template_string, request
import joblib
import pandas as pd
import os

# Initialize Flask app
app = Flask(__name__)

# Load model and encoders
model = joblib.load("calibrated_kabaddi_model.pkl")
team1_encoder = joblib.load("Team 1_encoder.pkl")
team2_encoder = joblib.load("Team 2_encoder.pkl")
outcome_encoder = joblib.load("Outcome_encoder.pkl")

# Define available teams
teams = [
    "Bengaluru Bulls", "Telugu Titans", "U Mumba", "U.P. Yoddhas",
    "Dabang Delhi K.C.", "Patna Pirates", "Puneri Paltan",
    "Jaipur Pink Panthers", "Tamil Thalaivas", "Bengal Warriors",
    "Gujarat Giants", "Haryana Steelers"
]

# Templates
home_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Kabaddi Win Predictor</title>
    <style>
        body {
            background: url('https://www.prokabaddi.com/static-assets/waf-images/9c/55/fd/16-9/1035-512/zhS4WDvpnK.jpg') no-repeat center center fixed;
            background-size: cover;
            color: white;
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            background: rgba(0, 0, 0, 0.8);
            padding: 20px 40px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
        }
        h1 {
            margin-bottom: 20px;
            font-size: 2em;
        }
        form {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        label, select, input {
            margin: 10px 0;
            width: 80%;
        }
        button {
            margin-top: 20px;
            padding: 10px 20px;
            background-color: #ff5722;
            border: none;
            border-radius: 5px;
            color: white;
            font-size: 1em;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        button:hover {
            background-color: #e64a19;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Kabaddi Win Predictor</h1>
        <form action="/predict" method="post">
            <label for="team1">Team 1:</label>
            <select id="team1" name="team1" required>
                <option value="" disabled selected>Select Team 1</option>
                {% for team in teams %}
                <option value="{{ team }}">{{ team }}</option>
                {% endfor %}
            </select>
            <label for="team2">Team 2:</label>
            <select id="team2" name="team2" required>
                <option value="" disabled selected>Select Team 2</option>
                {% for team in teams %}
                <option value="{{ team }}">{{ team }}</option>
                {% endfor %}
            </select>
            <label for="time_left">Time Left (minutes):</label>
            <input type="number" id="time_left" name="time_left" required>
            <label for="team1_score">Team 1 Score:</label>
            <input type="number" id="team1_score" name="team1_score" required>
            <label for="team2_score">Team 2 Score:</label>
            <input type="number" id="team2_score" name="team2_score" required>
            <label for="raid_success_1">Raid Success Rate (Team 1):</label>
            <input type="number" id="raid_success_1" name="raid_success_1" step="0.01" required>
            <label for="raid_success_2">Raid Success Rate (Team 2):</label>
            <input type="number" id="raid_success_2" name="raid_success_2" step="0.01" required>
            <label for="tackle_success_1">Tackle Success Rate (Team 1):</label>
            <input type="number" id="tackle_success_1" name="tackle_success_1" step="0.01" required>
            <label for="tackle_success_2">Tackle Success Rate (Team 2):</label>
            <input type="number" id="tackle_success_2" name="tackle_success_2" step="0.01" required>
            <button type="submit">Predict</button>
        </form>
    </div>
</body>
</html>
"""

result_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Prediction Result</title>
    <style>
        body {
            background: url('https://www.prokabaddi.com/static-assets/waf-images/9c/55/fd/16-9/1035-512/zhS4WDvpnK.jpg') no-repeat center center fixed;
            background-size: cover;
            color: white;
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            background: rgba(0, 0, 0, 0.8);
            padding: 20px 40px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
        }
        h1 {
            margin-bottom: 20px;
            font-size: 2em;
        }
        p {
            margin: 10px 0;
        }
        a {
            display: inline-block;
            margin-top: 20px;
            padding: 10px 20px;
            background-color: #ff5722;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            transition: background-color 0.3s ease;
        }
        a:hover {
            background-color: #e64a19;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Prediction Result</h1>
        <p>Team 1: {{ team1 }}</p>
        <p>Team 2: {{ team2 }}</p>
        <p>Predicted Outcome: {{ outcome }}</p>
        <p>Winning Chances:</p>
        <ul>
            <li>{{ team1 }}: {{ probability_team1 }}%</li>
            <li>{{ team2 }}: {{ probability_team2 }}%</li>
            <li>Draw: {{ probability_draw }}%</li>
        </ul>
        <a href="/">Go Back</a>
    </div>
</body>
</html>
"""

error_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Error</title>
</head>
<body>
    <h1>Oops! Something went wrong.</h1>
    <p>Error: {{ error_message }}</p>
    <a href="/">Go Back</a>
</body>
</html>
"""

# Routes
@app.route('/')
def home():
    return render_template_string(home_template, teams=teams)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input values
        team1 = request.form['team1']
        team2 = request.form['team2']
        time_left = float(request.form['time_left'])
        team1_score = int(request.form['team1_score'])
        team2_score = int(request.form['team2_score'])
        raid_success_1 = float(request.form['raid_success_1'])
        raid_success_2 = float(request.form['raid_success_2'])
        tackle_success_1 = float(request.form['tackle_success_1'])
        tackle_success_2 = float(request.form['tackle_success_2'])

        # Check if the same team is selected for both
        if team1 == team2:
            return render_template_string(error_template, error_message="Team 1 and Team 2 cannot be the same. Please select different teams.")

        # Encode teams
        team1_encoded = team1_encoder.transform([team1])[0]
        team2_encoded = team2_encoder.transform([team2])[0]

        # Prepare feature dataframe
        feature_names = [
            "Team 1", "Team 2", "Time Left",
            "Team 1 Score", "Team 2 Score", "Raid Success Rate 1",
            "Raid Success Rate 2", "Tackle Success Rate 1", "Tackle Success Rate 2"
        ]
        features = pd.DataFrame([[team1_encoded, team2_encoded, time_left, team1_score, team2_score,
                                  raid_success_1, raid_success_2, tackle_success_1, tackle_success_2]],
                                columns=feature_names)

        # Make prediction
        prediction = model.predict(features)[0]
        probabilities = model.predict_proba(features)[0]
        probability_team1 = probabilities[1] * 100
        probability_team2 = probabilities[0] * 100
        probability_draw = probabilities[2] * 100 if len(probabilities) > 2 else 0.0

        # Decode outcome
        decoded_outcome = outcome_encoder.inverse_transform([prediction])[0]

        return render_template_string(
            result_template,
            team1=team1,
            team2=team2,
            outcome=decoded_outcome,
            probability_team1=f"{probability_team1:.2f}",
            probability_team2=f"{probability_team2:.2f}",
            probability_draw=f"{probability_draw:.2f}"
        )
    except Exception as e:
        return render_template_string(error_template, error_message=f"Error: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)
