def assess_risk(fraud_probability):
    """
    Convert fraud probability into a risk level.
    """

    if fraud_probability >= 0.70:
        return "HIGH"
    elif fraud_probability >= 0.30:
        return "MEDIUM"
    else:
        return "LOW"


def recommend_action(risk_level):
    """
    Recommend an action based on the risk level.
    """

    if risk_level == "HIGH":
        return "BLOCK"

    elif risk_level == "MEDIUM":
        return "REVIEW"

    else:
        return "APPROVE"
