import pandas as pd
import mlflow
import mlflow.sklearn
import pickle
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# -----------------------------
# Create folders
# -----------------------------
os.makedirs("models", exist_ok=True)

# -----------------------------
# Load dataset
# -----------------------------
df = pd.read_csv("data/WA_Fn-UseC_-Telco-Customer-Churn.csv")

# -----------------------------
# Basic preprocessing
# -----------------------------
df = df.dropna()

# Convert TotalCharges to numeric (IMPORTANT fix)
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df = df.dropna()

# -----------------------------
# Encode categorical features
# -----------------------------
encoders = {}

for col in df.select_dtypes(include=['object']).columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le

# -----------------------------
# Split data
# -----------------------------
X = df.drop("Churn", axis=1)
y = df["Churn"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# -----------------------------
# Save feature columns
# -----------------------------
with open("models/features.pkl", "wb") as f:
    pickle.dump(X.columns.tolist(), f)

# -----------------------------
# Save encoders
# -----------------------------
with open("models/encoders.pkl", "wb") as f:
    pickle.dump(encoders, f)

# -----------------------------
# Train models
# -----------------------------
models = {
    "log_reg": LogisticRegression(max_iter=1000),
    "rf": RandomForestClassifier()
}

for name, model in models.items():
    with mlflow.start_run(run_name=name):
        model.fit(X_train, y_train)
        preds = model.predict(X_test)

        acc = accuracy_score(y_test, preds)

        mlflow.log_param("model", name)
        mlflow.log_metric("accuracy", acc)

        mlflow.sklearn.log_model(
            model,
            "model",
            registered_model_name="ChurnModel"
        )

print("✅ Training complete + models registered!")