# 🏆 Pro Kabaddi Match Win Prediction

A machine learning project that predicts the winning probability of a **Pro Kabaddi** match based on match statistics.  
It uses historical match data and real-time inputs such as raid and tackle success rates, match scores, and time remaining to predict which team is more likely to win.

---

## 📌 Features

- Predict win probability for **Team 1** and **Team 2**
- Web-based interface built with **Flask**
- Model calibration for improved accuracy
- Uses real **Pro Kabaddi** historical data for training
- Supports multiple model versions

---

## 📊 Model Input Factors

The prediction model considers:

1. **Team 1** – Selected from the Pro Kabaddi team list  
2. **Team 2** – Selected from the Pro Kabaddi team list  
3. **Time Left (minutes)** – Remaining time in the match  
4. **Team 1 Score** – Current score of Team 1  
5. **Team 2 Score** – Current score of Team 2  
6. **Raid Success Rate (Team 1)** – % of successful raids by Team 1  
7. **Raid Success Rate (Team 2)** – % of successful raids by Team 2  
8. **Tackle Success Rate (Team 1)** – % of successful tackles by Team 1  
9. **Tackle Success Rate (Team 2)** – % of successful tackles by Team 2  

---

## 📂 Project Structure

```
Pro Kabaddi Match Win Prediction/
│
├── app.py                        # Flask web app
├── calibrate_model.py            # Script to calibrate model
├── dpy.py                         # Data preprocessing functions
├── test_model.py                  # Test original model
├── test_calibrated_model.py       # Test calibrated model
├── verify_encoders.py             # Validate encoders
├── kabaddi_data.csv               # Historical match dataset
├── kabaddi_model.pkl              # Trained model
├── kabaddi_calibrated_model.pkl   # Calibrated model
├── kp4.pkl                        # Encoders/scalers/label mappings
├── home.html                      # Web interface template
└── scripts/                       # Additional scripts
```

---

## 🚀 How to Run Locally

1. **Clone the repository**  
```bash
git clone https://github.com/yourusername/Pro-Kabaddi-Match-Win-Prediction.git
cd Pro-Kabaddi-Match-Win-Prediction
```

2. **Install dependencies**  
```bash
pip install -r requirements.txt
```

3. **Run the app**  
```bash
python app.py
```

4. **Open in browser**  
Go to `http://127.0.0.1:5000/`

---

## 📜 License

This project currently **has no open-source license**.  
All rights are reserved by the author.  
Please contact the author for permission before using or modifying the code.
