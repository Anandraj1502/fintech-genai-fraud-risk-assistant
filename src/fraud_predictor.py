from pathlib import Path
import joblib
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "models" / "fraud_model.pkl"

FEATURES = [
    "type", "amount", "oldbalanceOrg", "newbalanceOrig",
    "oldbalanceDest", "newbalanceDest", "hour", "location"
]

def load_model():
    if not MODEL_PATH.exists():
        from src.train_model import train_model
        train_model()
    return joblib.load(MODEL_PATH)

def predict_transactions(df: pd.DataFrame) -> pd.DataFrame:
    model = load_model()
    working_df = df.copy()

    for col in FEATURES:
        if col not in working_df.columns:
            raise ValueError(f"Missing required column: {col}")

    probabilities = model.predict_proba(working_df[FEATURES])[:, 1]
    predictions = (probabilities >= 0.50).astype(int)

    working_df["fraud_probability"] = probabilities.round(4)
    working_df["risk_score"] = (probabilities * 100).round(2)
    working_df["prediction"] = predictions
    working_df["risk_level"] = working_df["risk_score"].apply(
        lambda x: "High Risk" if x >= 70 else "Medium Risk" if x >= 40 else "Low Risk"
    )
    return working_df
