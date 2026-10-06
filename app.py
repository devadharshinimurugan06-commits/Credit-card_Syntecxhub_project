import streamlit as st
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="FraudGuard AI",
    page_icon="💳",
    layout="wide"
)


# ============================================================
# SIMPLE UI
# ============================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #fff7fb,
        #ffeaf4,
        #f8efff
    );
}

.block-container {
    max-width: 1200px;
    padding-top: 40px;
}

.title {
    font-size: 42px;
    font-weight: 800;
    color: #9d175b;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 17px;
    color: #555555;
    margin-bottom: 30px;
}

.result-card {
    background: white;
    border-radius: 18px;
    padding: 25px;
    border: 1px solid #efc6da;
    box-shadow: 0 8px 25px rgba(120,30,90,0.08);
}

.result-number {
    font-size: 30px;
    font-weight: 800;
    color: #b31368;
}

.result-label {
    font-size: 13px;
    color: #666666;
    margin-bottom: 5px;
}

.stButton > button {
    width: 100%;
    border-radius: 10px;
    background: #c21875;
    color: white;
    font-weight: 700;
    border: none;
    padding: 12px;
}

.stButton > button:hover {
    background: #9d175b;
    color: white;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# DATASET
# ============================================================

DATA_URL = (
    "https://raw.githubusercontent.com/"
    "devadharshinimurugan06-commits/"
    "Credit-card_Syntecxhub_project/"
    "main/creditcard_small.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_dataset():

    df = pd.read_csv(DATA_URL)

    # Same cleaning used in the notebook
    df = df.drop_duplicates().reset_index(drop=True)

    return df


# ============================================================
# TRAIN XGBOOST
# ============================================================

@st.cache_resource
def train_model(df):

    X = df.drop("Class", axis=1)
    y = df["Class"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    model = XGBClassifier(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        eval_metric="logloss"
    )

    model.fit(X_train, y_train)

    return model


# ============================================================
# AGENTIC DECISION
# ============================================================

def fraud_agent(fraud_probability):

    # Threshold selected from the notebook
    threshold = 0.25

    # ML prediction using the selected threshold
    if fraud_probability >= threshold:
        prediction = 1
    else:
        prediction = 0

    # Agent risk assessment
    if fraud_probability >= 0.70:

        risk_level = "HIGH"
        action = "BLOCK"

    elif fraud_probability >= 0.30:

        risk_level = "MEDIUM"
        action = "REVIEW"

    else:

        risk_level = "LOW"
        action = "APPROVE"

    return prediction, risk_level, action


# ============================================================
# LOAD DATASET
# ============================================================

try:

    df = load_dataset()

except Exception as e:

    st.error("Unable to load the project CSV.")

    st.info(
        "Please check that creditcard_small.csv is available "
        "in the GitHub repository."
    )

    st.stop()


# ============================================================
# TRAIN MODEL
# ============================================================

try:

    model = train_model(df)

except Exception as e:

    st.error("Unable to train the XGBoost model.")

    st.exception(e)

    st.stop()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="title">💳 FraudGuard AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Credit Card Fraud Detection using XGBoost and Agentic AI'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# INPUT
# ============================================================

st.subheader("Transaction Input")

st.write(
    f"Project dataset loaded: **{len(df):,} transactions**"
)


# Select transaction row

row_number = st.number_input(
    "Select Transaction",
    min_value=1,
    max_value=len(df),
    value=1,
    step=1
)


selected_row = df.iloc[[int(row_number) - 1]]


# ============================================================
# OPTIONAL VIEW
# ============================================================

with st.expander("View selected transaction"):

    st.dataframe(
        selected_row.drop(columns=["Class"]),
        use_container_width=True
    )


# ============================================================
# DETECTION
# ============================================================

st.write("")

if st.button("🔍 Detect Fraud"):

    try:

        # Remove target column
        transaction = selected_row.drop(
            columns=["Class"]
        )

        # ----------------------------------------------------
        # ML MODEL
        # ----------------------------------------------------

        fraud_probability = model.predict_proba(
            transaction
        )[0][1]

        # ----------------------------------------------------
        # AGENT
        # ----------------------------------------------------

        prediction, risk_level, action = fraud_agent(
            fraud_probability
        )

        # ====================================================
        # OUTPUT
        # ====================================================

        st.divider()

        st.subheader("FraudGuard AI Result")

        col1, col2, col3 = st.columns(3)

        # ----------------------------------------------------
        # FRAUD PROBABILITY
        # ----------------------------------------------------

        with col1:

            st.markdown(
                '<div class="result-card">',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="result-label">'
                'FRAUD PROBABILITY'
                '</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div class="result-number">'
                f'{fraud_probability * 100:.2f}%'
                f'</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )

        # ----------------------------------------------------
        # PREDICTION
        # ----------------------------------------------------

        with col2:

            st.markdown(
                '<div class="result-card">',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="result-label">'
                'ML PREDICTION'
                '</div>',
                unsafe_allow_html=True
            )

            prediction_text = (
                "FRAUDULENT"
                if prediction == 1
                else "GENUINE"
            )

            st.markdown(
                f'<div class="result-number">'
                f'{prediction_text}'
                f'</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )

        # ----------------------------------------------------
        # ACTION
        # ----------------------------------------------------

        with col3:

            st.markdown(
                '<div class="result-card">',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="result-label">'
                'AGENT DECISION'
                '</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div class="result-number">'
                f'{action}'
                f'</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )

        # ====================================================
        # RISK
        # ====================================================

        st.write("")

        if risk_level == "HIGH":

            st.error(
                "🔴 HIGH RISK — Transaction should be BLOCKED."
            )

        elif risk_level == "MEDIUM":

            st.warning(
                "🟠 MEDIUM RISK — Transaction requires REVIEW."
            )

        else:

            st.success(
                "🟢 LOW RISK — Transaction can be APPROVED."
            )

        # ====================================================
        # SIMPLE AGENT OUTPUT
        # ====================================================

        st.write("")

        st.subheader("Agentic Risk Decision")

        st.write(
            f"**Risk Level:** {risk_level}"
        )

        st.write(
            f"**Recommended Action:** {action}"
        )

    except Exception as e:

        st.error("Fraud prediction failed.")

        st.exception(e)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "FraudGuard AI • Credit Card Fraud Detection"
)

st.caption(
    "Built by Devadharshini Murugan"
)
