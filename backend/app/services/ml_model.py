import numpy as np
import pickle
import os
from sklearn.ensemble import RandomForestClassifier

MODEL_PATH = "saved_models/model.pkl"


# -----------------------------
# FEATURE EXTRACTION
# -----------------------------
def extract_features(data: str):
    features = []

    features.append(len(data))
    features.append(data.count('@'))
    features.append(data.count('&'))
    features.append(data.count('='))

    features.append(1 if "http" in data else 0)

    suspicious_words = ["free", "win", "offer", "click"]
    features.append(1 if any(word in data.lower() for word in suspicious_words) else 0)

    features.append(1 if data.startswith("upi://pay") else 0)

    return np.array(features)


# -----------------------------
# TRAIN MODEL
# -----------------------------
def train_model():
    data = [
        ("upi://pay?pa=abc@ybl&pn=shop", 0),
        ("upi://pay?pa=test@okaxis&pn=store", 0),
        ("http://fake-link.com", 1),
        ("free-money-win-now", 1),
        ("upi://pay?pa=fraud@xyz&pn=hacker", 1),
    ]

    X = []
    y = []

    for text, label in data:
        X.append(extract_features(text))
        y.append(label)

    X = np.array(X)
    y = np.array(y)

    model = RandomForestClassifier()
    model.fit(X, y)

    os.makedirs("saved_models", exist_ok=True)

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)

    print("✅ Model trained and saved")


# -----------------------------
# LOAD MODEL
# -----------------------------
def load_model():
    if not os.path.exists(MODEL_PATH):
        print("⚠️ Model not found, training...")
        train_model()

    try:
        with open(MODEL_PATH, "rb") as f:
            return pickle.load(f)
    except:
        print("⚠️ Corrupted model, retraining...")
        train_model()
        with open(MODEL_PATH, "rb") as f:
            return pickle.load(f)


# -----------------------------
# LOAD MODEL (AFTER FUNCTIONS)
# -----------------------------
model = load_model()


# -----------------------------
# PREDICT
# -----------------------------
def predict(data: str):
    features = extract_features(data).reshape(1, -1)
    prediction = model.predict(features)[0]
    return prediction