import joblib
import pandas as pd

# Load trained fraud detection model
model = joblib.load("final_fraud_model.pkl")

# Features used by the model
FEATURE_COLUMNS = [
    "Time",
    "V1", "V2", "V3", "V4", "V5", "V6", "V7",
    "V8", "V9", "V10", "V11", "V12", "V13", "V14",
    "V15", "V16", "V17", "V18", "V19", "V20", "V21",
    "V22", "V23", "V24", "V25", "V26", "V27", "V28",
    "Amount"
]


def predict_fraud(transaction):
    """
    Predict whether a transaction is fraudulent.
    Returns fraud probability and prediction.
    """

    # Convert input into DataFrame
    data = pd.DataFrame([transaction])

    # Keep features in the correct order
    data = data[FEATURE_COLUMNS]

    # Fraud probability
    fraud_probability = model.predict_proba(data)[0][1]

    # Default model prediction
    prediction = model.predict(data)[0]

    return {
        "prediction": int(prediction),
        "fraud_probability": float(fraud_probability)
    }
