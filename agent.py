from tools import predict_fraud
from decision import assess_risk, recommend_action


def fraud_detection_agent(transaction):
    """
    Agentic workflow for credit card fraud detection.

    Flow:
    Transaction
        ↓
    Fraud Prediction Tool
        ↓
    Risk Assessment
        ↓
    Business Action
    """

    # Step 1: Get fraud prediction from the ML model
    prediction_result = predict_fraud(transaction)

    fraud_probability = prediction_result["fraud_probability"]
    prediction = prediction_result["prediction"]

    # Step 2: Assess risk
    risk_level = assess_risk(fraud_probability)

    # Step 3: Recommend business action
    action = recommend_action(risk_level)

    # Step 4: Return complete agent result
    return {
        "prediction": prediction,
        "fraud_probability": fraud_probability,
        "risk_level": risk_level,
        "recommended_action": action
    }
