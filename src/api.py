import random
import mlflow.pyfunc
from fastapi import FastAPI
import pandas as pd
import pickle
import logging

logging.basicConfig(filename="logs.txt", level=logging.INFO)

app = FastAPI()

# -----------------------------
# Load models from MLflow
# -----------------------------
model_A = mlflow.pyfunc.load_model("models:/ChurnModel@production")
model_B = mlflow.pyfunc.load_model("models:/ChurnModel@staging")

# -----------------------------
# Load features + encoders
# -----------------------------
with open("models/features.pkl", "rb") as f:
    feature_columns = pickle.load(f)

with open("models/encoders.pkl", "rb") as f:
    encoders = pickle.load(f)

# -----------------------------
# Prediction endpoint
# -----------------------------
@app.post("/predict")
def predict(data: dict):

    df = pd.DataFrame([data])

    # Encode categorical features
    for col, le in encoders.items():
        if col in df.columns:
            try:
                df[col] = le.transform(df[col])
            except:
                df[col] = 0  # fallback if unseen value

    # Add missing columns
    for col in feature_columns:
        if col not in df.columns:
            df[col] = 0

    # Ensure correct order
    df = df[feature_columns]

    # A/B testing
    if random.random() < 0.5:
        prediction = model_A.predict(df)
        model_used = "Production"
    else:
        prediction = model_B.predict(df)
        model_used = "Staging"

    logging.info(f"Model: {model_used}, Prediction: {int(prediction[0])}")    

    return {
        "prediction": int(prediction[0]),
        "model_used": model_used
    }


