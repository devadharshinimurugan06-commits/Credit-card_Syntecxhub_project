# ============================================================
# FraudGuard AI
# Credit Card Fraud Detection + Agentic AI
# Complete Streamlit App
# ============================================================

import os
import sys
from pathlib import Path
import importlib

import numpy as np
import pandas as pd
import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="FraudGuard AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# BASE DIRECTORY
# ============================================================

BASE_DIR = Path(__file__).resolve().parent


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- GLOBAL ---------- */

    .stApp {
        background: #fff7fb;
    }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    h1, h2, h3, h4, p, label, span, div {
        color: #202020;
    }

    /* ---------- SIDEBAR ---------- */

    [data-testid="stSidebar"] {
        background: #21151d;
    }

    [data-testid="stSidebar"] * {
        color: white !important;
    }

    /* ---------- HEADINGS ---------- */

    .main-title {
        font-size: 38px;
        font-weight: 900;
        color: #171717;
        margin-bottom: 4px;
    }

    .subtitle {
        font-size: 17px;
        color: #555555;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 27px;
        font-weight: 850;
        color: #171717;
        margin-top: 10px;
        margin-bottom: 8px;
    }

    .section-description {
        font-size: 15px;
        color: #555555;
        margin-bottom: 20px;
    }

    /* ---------- CARDS ---------- */

    .info-card {
        background: white;
        border: 1px solid #efd0df;
        border-radius: 16px;
        padding: 22px;
        margin: 12px 0;
        box-shadow: 0 5px 18px rgba(100, 30, 70, 0.06);
    }

    .info-card h3 {
        margin-top: 0;
        color: #8f1858;
    }

    .info-card p {
        color: #444444;
        line-height: 1.6;
    }

    .metric-card {
        background: white;
        border: 1px solid #efd0df;
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 5px 18px rgba(100, 30, 70, 0.06);
    }

    .metric-number {
        font-size: 28px;
        font-weight: 900;
        color: #8f1858;
    }

    .metric-label {
        font-size: 14px;
        color: #555555;
        margin-top: 4px;
    }

    /* ---------- BUTTON ---------- */

    .stButton > button {
        width: 100%;
        border-radius: 12px;
        border: none;
        padding: 12px 20px;
        background: linear-gradient(90deg, #c81769, #8d28bd);
        color: white !important;
        font-weight: 800;
        font-size: 16px;
        box-shadow: 0 8px 18px rgba(150, 30, 110, 0.20);
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 10px 22px rgba(150, 30, 110, 0.28);
    }

    /* ---------- INPUTS ---------- */

    div[data-baseweb="select"] > div {
        border-radius: 10px;
    }

    div[data-testid="stNumberInput"] input {
        border-radius: 10px;
    }

    /* ---------- RESULT ---------- */

    .result-card {
        background: white;
        border: 2px solid #e6bfd2;
        border-radius: 18px;
        padding: 24px;
        margin-top: 20px;
        box-shadow: 0 8px 25px rgba(100, 30, 70, 0.08);
    }

    .result-title {
        font-size: 22px;
        font-weight: 850;
        color: #8f1858;
        margin-bottom: 15px;
    }

    .risk-high {
        background: #ffe5e5;
        border-left: 5px solid #d71920;
        padding: 14px;
        border-radius: 10px;
        font-weight: 800;
    }

    .risk-medium {
        background: #fff1d6;
        border-left: 5px solid #e28b00;
        padding: 14px;
        border-radius: 10px;
        font-weight: 800;
    }

    .risk-low {
        background: #e3f7e9;
        border-left: 5px solid #238636;
        padding: 14px;
        border-radius: 10px;
        font-weight: 800;
    }

    /* ---------- FOOTER ---------- */

    .footer {
        text-align: center;
        padding: 30px 0 10px 0;
        color: #666666 !important;
        font-size: 13px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# MODEL / AGENT DISCOVERY
# ============================================================

MODEL_CANDIDATES = [
    "final_fraud_model.pkl",
    "fraud_model.pkl",
    "xgboost_fraud_model.pkl",
    "best_fraud_model.pkl"
]


def find_model_file():
    """
    Find the fraud model inside the project folder.
    """

    # First check exact expected filenames
    for filename in MODEL_CANDIDATES:
        path = BASE_DIR / filename

        if path.exists():
            return path

    # Check common folders
    for folder in ["models", "model", "artifacts", "saved_models"]:

        folder_path = BASE_DIR / folder

        if not folder_path.exists():
            continue

        for filename in MODEL_CANDIDATES:

            path = folder_path / filename

            if path.exists():
                return path

    # Last fallback: search recursively
    for path in BASE_DIR.rglob("*.pkl"):

        name = path.name.lower()

        if (
            "fraud" in name
            or "xgb" in name
            or "model" in name
        ):
            return path

    return None


MODEL_PATH = find_model_file()


# ============================================================
# LOAD AGENT
# ============================================================

fraud_detection_agent = None
agent_import_error = None


def load_agent():

    global fraud_detection_agent
    global agent_import_error

    if fraud_detection_agent is not None:
        return fraud_detection_agent

    # The current tools.py uses:
    #
    # joblib.load("final_fraud_model.pkl")
    #
    # Therefore temporarily change working directory
    # to the model directory while importing the agent.

    original_cwd = os.getcwd()

    try:

        if MODEL_PATH is not None:
            os.chdir(MODEL_PATH.parent)

        # Try agent.py first
        try:

            agent_module = importlib.import_module("agent")

            fraud_detection_agent = getattr(
                agent_module,
                "fraud_detection_agent"
            )

        except Exception as first_error:

            # Try agents.py if project uses plural filename
            try:

                agents_module = importlib.import_module("agents")

                fraud_detection_agent = getattr(
                    agents_module,
                    "fraud_detection_agent"
                )

            except Exception as second_error:

                agent_import_error = (
                    f"agent.py error: {first_error}\n\n"
                    f"agents.py error: {second_error}"
                )

    except Exception as e:

        agent_import_error = str(e)

    finally:

        os.chdir(original_cwd)

    return fraud_detection_agent


load_agent()


# ============================================================
# FEATURE COLUMNS
# ============================================================

DEFAULT_FEATURE_COLUMNS = (
    ["Time"]
    + [f"V{i}" for i in range(1, 29)]
    + ["Amount"]
)


def get_feature_columns():

    try:

        tools_module = importlib.import_module("tools")

        columns = getattr(
            tools_module,
            "FEATURE_COLUMNS",
            None
        )

        if columns is not None:

            return list(columns)

    except Exception:
        pass

    return DEFAULT_FEATURE_COLUMNS


FEATURE_COLUMNS = get_feature_columns()


# ============================================================
# DATASET DISCOVERY
# ============================================================

DATASET_CANDIDATES = [
    "creditcard_small.csv",
    "creditcard.csv",
    "credit_card.csv",
    "credit_card_data.csv",
    "fraud_dataset.csv"
]


def find_dataset():

    # Root folder
    for filename in DATASET_CANDIDATES:

        path = BASE_DIR / filename

        if path.exists():
            return path

    # Common folders
    for folder in ["data", "dataset", "datasets"]:

        folder_path = BASE_DIR / folder

        if not folder_path.exists():
            continue

        for filename in DATASET_CANDIDATES:

            path = folder_path / filename

            if path.exists():
                return path

    # Recursive search
    for path in BASE_DIR.rglob("*.csv"):

        name = path.name.lower()

        if (
            "creditcard" in name
            or "credit_card" in name
            or "fraud" in name
        ):
            return path

    return None


DATASET_PATH = find_dataset()


@st.cache_data
def load_project_dataset(path_string):

    return pd.read_csv(path_string)


# ============================================================
# RESULT HELPERS
# ============================================================

def normalize_probability(value):

    try:

        probability = float(value)

    except Exception:

        return 0.0

    # If model/agent gives percentage such as 94.5
    if probability > 1:

        probability = probability / 100

    probability = max(
        0.0,
        min(1.0, probability)
    )

    return probability


def get_result_value(result, *keys, default=None):

    if not isinstance(result, dict):
        return default

    for key in keys:

        if key in result:
            return result[key]

    return default


def normalize_prediction(value):

    if value is None:
        return "Unknown"

    text = str(value).strip()

    if text.lower() in ["1", "fraud", "true", "yes"]:
        return "Fraud"

    if text.lower() in ["0", "legitimate", "genuine", "false", "no"]:
        return "Legitimate"

    return text


def normalize_risk(value):

    if value is None:
        return "Unknown"

    return str(value).strip().upper()


def normalize_action(value):

    if value is None:
        return "Not Available"

    return str(value).strip().upper()


# ============================================================
# DISPLAY RESULT
# ============================================================

def display_prediction_result(result):

    if result is None:

        st.error(
            "The fraud detection agent did not return a result."
        )

        return

    probability = normalize_probability(
        get_result_value(
            result,
            "fraud_probability",
            "probability",
            "fraud_prob",
            default=0
        )
    )

    prediction = normalize_prediction(
        get_result_value(
            result,
            "prediction",
            "predicted_class",
            "class",
            "fraud_prediction"
        )
    )

    risk = normalize_risk(
        get_result_value(
            result,
            "risk_level",
            "risk",
            default="UNKNOWN"
        )
    )

    action = normalize_action(
        get_result_value(
            result,
            "recommended_action",
            "action",
            "decision",
            default="Not Available"
        )
    )

    st.markdown(
        "### 🛡️ FraudGuard AI Result"
    )

    r1, r2, r3, r4 = st.columns(4)

    with r1:

        st.metric(
            "Fraud Probability",
            f"{probability * 100:.2f}%"
        )

    with r2:

        st.metric(
            "ML Prediction",
            prediction
        )

    with r3:

        st.metric(
            "Risk Level",
            risk
        )

    with r4:

        st.metric(
            "Recommended Action",
            action
        )

    # Progress
    st.progress(
        probability,
        text=f"Fraud probability: {probability * 100:.2f}%"
    )

    # Risk message
    if "HIGH" in risk:

        st.error(
            f"🔴 HIGH RISK — Recommended action: {action}"
        )

    elif "MEDIUM" in risk:

        st.warning(
            f"🟠 MEDIUM RISK — Recommended action: {action}"
        )

    elif "LOW" in risk:

        st.success(
            f"🟢 LOW RISK — Recommended action: {action}"
        )

    else:

        st.info(
            f"Risk: {risk} | Recommended action: {action}"
        )


    # ========================================================
    # AGENT ANALYSIS
    # ========================================================

    st.markdown("### 🤖 Agent Analysis")

    probability_percent = probability * 100

    if "HIGH" in risk:

        st.info(
            f"The agent returned a fraud probability of "
            f"**{probability_percent:.2f}%**, with an ML prediction of "
            f"**{prediction}**. The agent assessed the transaction as "
            f"**{risk} risk** and recommended **{action}**."
        )

    elif "MEDIUM" in risk:

        st.info(
            f"The agent returned a fraud probability of "
            f"**{probability_percent:.2f}%**, with an ML prediction of "
            f"**{prediction}**. The agent assessed the transaction as "
            f"**{risk} risk** and recommended **{action}**."
        )

    elif "LOW" in risk:

        st.info(
            f"The agent returned a fraud probability of "
            f"**{probability_percent:.2f}%**, with an ML prediction of "
            f"**{prediction}**. The agent assessed the transaction as "
            f"**{risk} risk** and recommended **{action}**."
        )

    else:

        st.info(
            f"The agent returned a fraud probability of "
            f"**{probability_percent:.2f}%**, with an ML prediction of "
            f"**{prediction}**. The agent assessed the transaction as "
            f"**{risk} risk** and recommended **{action}**."
        )


    # ========================================================
    # AGENT DECISION PATH
    # ========================================================

    st.markdown("### 🔄 Agent Decision Path")

    d1, d2, d3, d4 = st.columns(4)

    with d1:

        st.metric(
            "Model Output",
            f"{probability_percent:.2f}%"
        )

    with d2:

        st.metric(
            "Risk Assessment",
            risk
        )

    with d3:

        st.metric(
            "ML Prediction",
            prediction
        )

    with d4:

        st.metric(
            "Final Decision",
            action
        )


    # ========================================================
    # ORIGINAL AGENT OUTPUT
    # ========================================================

    with st.expander("🤖 View Agent Execution Details"):

        if isinstance(result, dict):

            clean_result = {}

            for key, value in result.items():

                if isinstance(value, (np.integer, np.floating)):
                    value = value.item()

                clean_result[key] = value

            st.json(clean_result)

        else:

            st.write(result)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            background:linear-gradient(135deg,#7d174f,#a82b75);
            padding:22px;
            border-radius:18px;
            margin-bottom:20px;
        ">

        <div style="
            font-size:25px;
            font-weight:900;
            color:white;
        ">
        🛡️ FraudGuard AI
        </div>

        <div style="
            font-size:13px;
            color:#ffe8f4;
            margin-top:5px;
        ">
        Intelligent Credit Card Fraud Detection
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### Navigation")

    page = st.radio(
        "Navigate",
        [
            "🏠 Dashboard",
            "🔍 Fraud Detection",
            "🤖 Agentic AI",
            "ℹ️ About Project"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")

    st.markdown("### System Status")

    if MODEL_PATH is not None:

        st.success("Model Found")

        st.caption(
            f"Model: {MODEL_PATH.name}"
        )

    else:

        st.error("Model Not Found")

    if fraud_detection_agent is not None:

        st.success("Agent Ready")

    else:

        st.error("Agent Not Loaded")


# ============================================================
# DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    st.markdown(
        '<div class="main-title">🛡️ FraudGuard AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="subtitle">
        AI-powered credit card fraud detection with automated
        risk assessment and business decision support.
        </div>
        """,
        unsafe_allow_html=True
    )

    # Model metrics
    st.markdown(
        "### 📊 Model Performance"
    )

    m1, m2, m3, m4 = st.columns(4)

    with m1:

        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-number">98.73%</div>
                <div class="metric-label">Precision</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with m2:

        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-number">82.11%</div>
                <div class="metric-label">Recall</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with m3:

        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-number">89.66%</div>
                <div class="metric-label">F1 Score</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with m4:

        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-number">98.35%</div>
                <div class="metric-label">ROC-AUC</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    # Objective
    st.markdown(
        """
        <div class="info-card">

        <h3>🚀 Project Objective</h3>

        <p>
        FraudGuard AI is designed to identify potentially fraudulent
        credit card transactions and support faster financial
        decision-making.
        </p>

        <p>
        The system combines machine learning prediction with
        risk assessment and business-action recommendation.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    # Dataset Insights
    st.markdown("### 📊 Dataset Insights")

    d1, d2, d3, d4 = st.columns(4)

    with d1:

        st.metric(
            "Transaction Features",
            "30"
        )

    with d2:

        st.metric(
            "Main Features",
            "Time + V1–V28 + Amount"
        )

    with d3:

        st.metric(
            "Target Column",
            "Class"
        )

    with d4:

        st.metric(
            "Prediction Type",
            "Binary Classification"
        )

    st.markdown(
        """
        <div class="info-card">

        <h3>🔎 Understanding the Dataset</h3>

        <p>
        The dataset contains credit card transaction records used
        to identify whether a transaction is legitimate or fraudulent.
        </p>

        <p>
        The model uses <b>Time</b>, <b>V1–V28</b> and
        <b>Amount</b> as transaction features. The
        <b>Class</b> column represents the target used for
        fraud classification and is not passed as an input feature
        during prediction.
        </p>

        <p>
        The transaction data is given to the trained ML model.
        The resulting fraud probability is then returned through
        the agentic workflow as the risk assessment and recommended
        business action.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    # Workflow
    st.markdown("### 🔄 Fraud Detection Workflow")

    w1, w2, w3, w4 = st.columns(4)

    with w1:

        st.info(
            "1️⃣ Transaction\n\n"
            "Transaction data is provided to the system."
        )

    with w2:

        st.info(
            "2️⃣ ML Prediction\n\n"
            "The trained fraud model predicts fraud probability."
        )

    with w3:

        st.info(
            "3️⃣ Risk Assessment\n\n"
            "Probability is converted into a risk level."
        )

    with w4:

        st.info(
            "4️⃣ Business Decision\n\n"
            "The system recommends Approve, Review or Block."
        )


# ============================================================
# FRAUD DETECTION
# ============================================================

elif page == "🔍 Fraud Detection":

    st.markdown(
        '<div class="main-title">🔍 Fraud Detection</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="subtitle">
        Select a transaction from the project dataset or enter
        transaction values manually.
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # INPUT METHOD
    # --------------------------------------------------------

    input_method = st.radio(
        "Choose transaction input",
        [
            "Select from Project Dataset",
            "Manual Input"
        ],
        horizontal=True
    )

    transaction = None

    # --------------------------------------------------------
    # DATASET INPUT
    # --------------------------------------------------------

    if input_method == "Select from Project Dataset":

        st.markdown("### 📂 Project Dataset")

        if DATASET_PATH is None:

            st.error(
                "Project dataset was not found."
            )

            st.info(
                "Add your credit card CSV file to the same "
                "GitHub repository as app.py."
            )

        else:

            try:

                df = load_project_dataset(
                    str(DATASET_PATH)
                )

                st.success(
                    f"Dataset loaded: {DATASET_PATH.name} "
                    f"({len(df):,} transactions)"
                )

                # --------------------------------------------
                # Transaction selector
                # --------------------------------------------

                if len(df) <= 5000:

                    selected_label = st.selectbox(
                        "Select Transaction",
                        [
                            f"Transaction {i + 1}"
                            for i in range(len(df))
                        ]
                    )

                    selected_index = int(
                        selected_label.split()[-1]
                    ) - 1

                else:

                    st.info(
                        "Large dataset detected. "
                        "Use the transaction number below."
                    )

                    selected_index = st.number_input(
                        "Transaction number",
                        min_value=1,
                        max_value=len(df),
                        value=1,
                        step=1
                    ) - 1

                selected_row = df.iloc[
                    int(selected_index)
                ]

                # Show selected transaction
                st.markdown("### 👁️ Selected Transaction")

                display_row = selected_row.to_frame().T

                st.dataframe(
                    display_row,
                    width="stretch",
                    hide_index=True
                )

                # Remove target column
                transaction_series = selected_row.copy()

                if "Class" in transaction_series.index:

                    transaction_series = transaction_series.drop(
                        "Class"
                    )

                if "class" in transaction_series.index:

                    transaction_series = transaction_series.drop(
                        "class"
                    )

                transaction = transaction_series.to_dict()

            except Exception as e:

                st.error(
                    f"Unable to load project dataset: {e}"
                )


    # --------------------------------------------------------
    # MANUAL INPUT
    # --------------------------------------------------------

    else:

        st.markdown("### ✍️ Manual Transaction Input")

        st.caption(
            "Enter the transaction features required by the fraud model."
        )

        # Time + Amount
        c1, c2 = st.columns(2)

        with c1:

            time_value = st.number_input(
                "Time",
                value=0.0,
                step=1.0
            )

        with c2:

            amount_value = st.number_input(
                "Amount",
                value=100.0,
                min_value=0.0,
                step=10.0
            )

        transaction = {}

        transaction["Time"] = time_value

        # V1-V28
        st.markdown("### 🔢 Transaction Features")

        v_columns = [
            f"V{i}"
            for i in range(1, 29)
        ]

        for start in range(0, 28, 4):

            cols = st.columns(4)

            for j, col in enumerate(
                v_columns[start:start + 4]
            ):

                with cols[j]:

                    transaction[col] = st.number_input(
                        col,
                        value=0.0,
                        step=0.01,
                        format="%.6f",
                        key=f"manual_{col}"
                    )

        transaction["Amount"] = amount_value

    # --------------------------------------------------------
    # PREDICT
    # --------------------------------------------------------

    st.write("")

    if st.button(
        "🚀 Predict Fraud Risk",
        type="primary",
        width="stretch"
    ):

        if transaction is None:

            st.warning(
                "Please provide a transaction first."
            )

        elif fraud_detection_agent is None:

            st.error(
                "Fraud detection agent is not available."
            )

            if agent_import_error:

                st.code(
                    agent_import_error
                )

            if MODEL_PATH is None:

                st.warning(
                    "The trained model file was not found "
                    "inside the deployed repository."
                )

        else:

            try:

                # --------------------------------------------
                # Ensure numeric values
                # --------------------------------------------

                cleaned_transaction = {}

                for key, value in transaction.items():

                    try:

                        cleaned_transaction[key] = float(value)

                    except Exception:

                        cleaned_transaction[key] = value

                # --------------------------------------------
                # Run actual agent
                # --------------------------------------------

                with st.spinner(
                    "Running FraudGuard AI..."
                ):

                    result = fraud_detection_agent(
                        cleaned_transaction
                    )

                # --------------------------------------------
                # Show result directly below button
                # --------------------------------------------

                display_prediction_result(
                    result
                )

            except Exception as e:

                st.error(
                    "Prediction failed."
                )

                st.code(
                    str(e)
                )

                st.info(
                    "Check that the transaction columns match "
                    "the features expected by the trained model."
                )


# ============================================================
# AGENTIC AI
# ============================================================

elif page == "🤖 Agentic AI":

    st.markdown(
        '<div class="main-title">🤖 Agentic AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="subtitle">
        FraudGuard AI uses an agent-based workflow to convert
        machine-learning predictions into actionable business decisions.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 🔄 Agent Workflow")

    a1, a2, a3, a4 = st.columns(4)

    with a1:

        st.info(
            "📥 Transaction\n\n"
            "Receives the transaction features."
        )

    with a2:

        st.info(
            "🧠 Fraud Prediction\n\n"
            "The trained ML model generates fraud probability."
        )

    with a3:

        st.info(
            "🎯 Risk Assessment\n\n"
            "The probability is converted into LOW, MEDIUM or HIGH risk."
        )

    with a4:

        st.info(
            "🚦 Business Decision\n\n"
            "The system recommends APPROVE, REVIEW or BLOCK."
        )

    st.write("")

    # Tool 1
    st.markdown(
        """
        <div class="info-card">

        <h3>🧠 Tool 1 — Fraud Prediction</h3>

        <p>
        The trained machine-learning model analyzes the transaction
        features and produces a fraud probability.
        </p>

        <p>
        <b>Input:</b> Transaction features
        </p>

        <p>
        <b>Output:</b> Fraud probability + prediction
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    # Tool 2
    st.markdown(
        """
        <div class="info-card">

        <h3>🎯 Tool 2 — Risk Assessment</h3>

        <p>
        The fraud probability is interpreted as a business risk level.
        </p>

        <p>
        <b>LOW:</b> below 30% &nbsp;&nbsp;
        <b>MEDIUM:</b> 30% to below 70% &nbsp;&nbsp;
        <b>HIGH:</b> 70% or above
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    # Tool 3
    st.markdown(
        """
        <div class="info-card">

        <h3>🚦 Tool 3 — Business Decision</h3>

        <p>
        The agent converts the risk level into an operational
        recommendation.
        </p>

        <p>
        <b>LOW → APPROVE</b><br>
        <b>MEDIUM → REVIEW</b><br>
        <b>HIGH → BLOCK</b>
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    st.success(
        "The actual agent is executed from the Fraud Detection tab. "
        "This tab explains the agent architecture and workflow."
    )


# ============================================================
# ABOUT PROJECT
# ============================================================

elif page == "ℹ️ About Project":

    st.markdown(
        '<div class="main-title">ℹ️ About Project</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="subtitle">
        Credit Card Fraud Detection using Machine Learning
        and Agentic AI.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="info-card">

        <h3>🛡️ FraudGuard AI</h3>

        <p>
        FraudGuard AI is a machine-learning based fraud detection
        application designed to identify potentially fraudulent
        credit card transactions.
        </p>

        <p>
        The application combines a trained fraud detection model
        with an agentic decision workflow for risk assessment
        and recommended business action.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 🧰 Technology Stack")

    t1, t2, t3, t4 = st.columns(4)

    with t1:
        st.info("🐍 Python")

    with t2:
        st.info("📊 Pandas")

    with t3:
        st.info("🤖 Machine Learning")

    with t4:
        st.info("🎈 Streamlit")

    st.write("")

    st.markdown("### 📌 Project Components")

    components = pd.DataFrame(
        {
            "Component": [
                "Machine Learning Model",
                "Fraud Prediction",
                "Risk Assessment",
                "Business Decision",
                "Web Application"
            ],
            "Purpose": [
                "Detect fraudulent transactions",
                "Generate fraud probability",
                "Determine risk level",
                "Recommend operational action",
                "Provide an interactive interface"
            ]
        }
    )

    st.dataframe(
        components,
        width="stretch",
        hide_index=True
    )

    st.write("")

    st.markdown(
        """
        <div class="footer">
        FraudGuard AI • Credit Card Fraud Detection • Machine Learning + Agentic AI
        </div>
        """,
        unsafe_allow_html=True
    )
