import os
import joblib
import pandas as pd
import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="FraudGuard AI",
    page_icon="💳",
    layout="wide"
)


# ============================================================
# SIMPLE CSS
# ============================================================

st.markdown("""
<style>

.main {
    background-color: #fff7fc;
}

h1 {
    color: #9d175b;
}

h2, h3 {
    color: #9d175b;
}

.stButton > button {
    background-color: #c21875;
    color: white;
    border-radius: 8px;
    border: none;
    padding: 10px 22px;
    font-weight: 600;
}

.stButton > button:hover {
    background-color: #9d175b;
    color: white;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# MODEL LOADING
# ============================================================

@st.cache_resource
def load_model():

    possible_models = [
        "best_xgboost_model.pkl",
        "xgboost_model.pkl",
        "best_model.pkl",
        "best_classification_model.pkl",
        "fraud_model.pkl",
        "model.pkl"
    ]

    for model_file in possible_models:

        if os.path.exists(model_file):
            return joblib.load(model_file), model_file

    return None, None


model, model_name = load_model()


# ============================================================
# TARGET COLUMN DETECTION
# ============================================================

def find_target_column(df):

    possible_targets = [
        "Class",
        "class",
        "Fraud",
        "fraud",
        "is_fraud",
        "Is_Fraud",
        "fraud_flag",
        "Fraud_Flag",
        "target",
        "Target"
    ]

    for col in possible_targets:
        if col in df.columns:
            return col

    return None


# ============================================================
# AGENTIC RISK DECISION
# ============================================================

def fraud_agent(fraud_probability):

    probability = fraud_probability * 100

    if probability >= 80:

        decision = "BLOCK"
        risk = "HIGH"

    elif probability >= 40:

        decision = "REVIEW"
        risk = "MEDIUM"

    else:

        decision = "APPROVE"
        risk = "LOW"

    return risk, decision, probability


# ============================================================
# PREDICTION FUNCTION
# ============================================================

def make_prediction(transaction):

    input_data = transaction.copy()

    # Remove target if it exists
    target_col = find_target_column(input_data)

    if target_col is not None:
        input_data = input_data.drop(columns=[target_col])

    # Remove common index columns
    unwanted_columns = [
        "Unnamed: 0",
        "index",
        "Index"
    ]

    input_data = input_data.drop(
        columns=[c for c in unwanted_columns if c in input_data.columns],
        errors="ignore"
    )

    # Convert categorical columns where possible
    for col in input_data.columns:

        if input_data[col].dtype == "object":

            input_data[col] = pd.to_numeric(
                input_data[col],
                errors="coerce"
            )

    input_data = input_data.fillna(0)

    # --------------------------------------------------------
    # Align columns with model feature names if available
    # --------------------------------------------------------

    if hasattr(model, "feature_names_in_"):

        expected_features = list(model.feature_names_in_)

        for col in expected_features:

            if col not in input_data.columns:
                input_data[col] = 0

        input_data = input_data[expected_features]

    # --------------------------------------------------------
    # Prediction
    # --------------------------------------------------------

    prediction = model.predict(input_data)[0]

    # --------------------------------------------------------
    # Fraud probability
    # --------------------------------------------------------

    if hasattr(model, "predict_proba"):

        probabilities = model.predict_proba(input_data)[0]

        classes = list(model.classes_)

        # Find fraud class
        fraud_index = None

        for possible_class in [1, "1", "Fraud", "fraud", "TRUE", True]:

            if possible_class in classes:
                fraud_index = classes.index(possible_class)
                break

        if fraud_index is not None:
            fraud_probability = probabilities[fraud_index]
        else:
            # For binary classification, use second probability
            fraud_probability = (
                probabilities[1]
                if len(probabilities) > 1
                else probabilities[0]
            )

    else:

        fraud_probability = float(prediction)

    return prediction, fraud_probability


# ============================================================
# HEADER
# ============================================================

st.title("💳 FraudGuard AI")

st.write(
    "Credit Card Fraud Detection using Machine Learning "
    "and Agentic AI risk decision support."
)


# ============================================================
# MODEL STATUS
# ============================================================

if model is None:

    st.error(
        "Fraud detection model not found. "
        "Please place your trained XGBoost .pkl model "
        "in the same folder as app.py."
    )

    st.stop()


# ============================================================
# CSV INPUT
# ============================================================

st.subheader("Transaction Input")

uploaded_file = st.file_uploader(
    "Upload Transaction CSV",
    type=["csv"]
)


# ============================================================
# LOAD CSV
# ============================================================

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.success(
        f"CSV loaded successfully — {len(df):,} transactions found."
    )

else:

    possible_csv_files = [
        "credit_card.csv",
        "creditcard.csv",
        "fraud_detection.csv",
        "transactions.csv",
        "transaction.csv",
        "project.csv",
        "data.csv"
    ]

    df = None

    for csv_file in possible_csv_files:

        if os.path.exists(csv_file):

            df = pd.read_csv(csv_file)

            st.success(
                f"Project CSV loaded — {len(df):,} transactions found."
            )

            break

    if df is None:

        st.info(
            "Please upload your transaction CSV file to start fraud detection."
        )

        st.stop()


# ============================================================
# TRANSACTION SELECTION
# ============================================================

st.subheader("Select Transaction")

row_number = st.number_input(
    "Transaction Row",
    min_value=1,
    max_value=len(df),
    value=1,
    step=1
)

selected_index = row_number - 1

transaction = df.iloc[[selected_index]].copy()


# ============================================================
# SHOW INPUT DATA
# ============================================================

with st.expander("View Transaction Data"):

    st.dataframe(
        transaction,
        use_container_width=True
    )


# ============================================================
# DETECTION BUTTON
# ============================================================

if st.button("🔍 Detect Fraud"):

    try:

        prediction, fraud_probability = make_prediction(
            transaction
        )

        # ----------------------------------------------------
        # Agentic risk assessment
        # ----------------------------------------------------

        risk, decision, probability = fraud_agent(
            fraud_probability
        )

        st.divider()

        st.subheader("Fraud Detection Result")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Fraud Probability",
                f"{probability:.2f}%"
            )

        with col2:

            st.metric(
                "Risk Level",
                risk
            )

        with col3:

            st.metric(
                "Agent Decision",
                decision
            )

        st.divider()

        # ====================================================
        # FINAL AGENT OUTPUT
        # ====================================================

        st.subheader("Agentic Risk Decision")

        if decision == "BLOCK":

            st.error(
                "🚨 HIGH RISK — Transaction should be BLOCKED."
            )

        elif decision == "REVIEW":

            st.warning(
                "⚠️ MEDIUM RISK — Transaction requires MANUAL REVIEW."
            )

        else:

            st.success(
                "✅ LOW RISK — Transaction can be APPROVED."
            )

        st.write(
            f"**Fraud Probability:** {probability:.2f}%"
        )

        st.write(
            f"**Risk Assessment:** {risk}"
        )

        st.write(
            f"**Final Decision:** {decision}"
        )

    except Exception as e:

        st.error(
            "Prediction failed."
        )

        st.exception(e)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "FraudGuard AI • Credit Card Fraud Detection & Agentic Risk Decision System"
)

st.caption(
    "Built by Devadharshini Murugan"
)
