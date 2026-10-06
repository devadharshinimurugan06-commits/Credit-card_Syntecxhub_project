import os
from pathlib import Path
import importlib

import pandas as pd
import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="FraudGuard AI",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).resolve().parent


# ============================================================
# FIND TRAINED MODEL
# ============================================================

MODEL_NAMES = [
    "final_fraud_model.pkl",
    "fraud_model.pkl",
    "xgboost_fraud_model.pkl",
    "best_fraud_model.pkl",
]


def find_model():
    # First check repository root
    for name in MODEL_NAMES:
        path = BASE_DIR / name

        if path.exists():
            return path

    # Then check folders inside repository
    for name in MODEL_NAMES:
        matches = list(BASE_DIR.rglob(name))

        if matches:
            return matches[0]

    # Last fallback: fraud/xgb related pickle
    matches = [
        path
        for path in BASE_DIR.rglob("*.pkl")
        if (
            "fraud" in path.name.lower()
            or "xgb" in path.name.lower()
        )
    ]

    if matches:
        return matches[0]

    return None


MODEL_PATH = find_model()


# ============================================================
# LOAD EXISTING AGENT
# ============================================================

fraud_detection_agent = None
agent_load_error = None


if MODEL_PATH is not None:

    original_cwd = Path.cwd()

    try:

        # IMPORTANT:
        # Your tools.py currently loads:
        # joblib.load("final_fraud_model.pkl")
        #
        # So temporarily change working directory to the
        # model's folder before importing the agent.

        os.chdir(MODEL_PATH.parent)

        try:
            agent_module = importlib.import_module("agent")
        except ModuleNotFoundError:
            agent_module = importlib.import_module("agents")

        fraud_detection_agent = getattr(
            agent_module,
            "fraud_detection_agent"
        )

    except Exception as e:

        agent_load_error = str(e)

    finally:

        os.chdir(original_cwd)

else:

    agent_load_error = (
        "No fraud model .pkl file was found "
        "inside the repository."
    )


# ============================================================
# MODEL FEATURE COLUMNS
# ============================================================

DEFAULT_FEATURES = (
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

        if columns:
            return list(columns)

    except Exception:
        pass

    return DEFAULT_FEATURES


FEATURE_COLUMNS = get_feature_columns()


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ================================
       MAIN BACKGROUND
       ================================ */

    .stApp {
        background:
            linear-gradient(
                135deg,
                #fff8fc 0%,
                #fdebf5 55%,
                #f7efff 100%
            );
    }


    /* ================================
       HEADER
       ================================ */

    [data-testid="stHeader"] {
        background: rgba(255,255,255,0);
    }


    /* ================================
       MAIN CONTENT
       ================================ */

    .main .block-container {
        max-width: 1350px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }


    /* ================================
       DARK TEXT
       ================================ */

    h1,
    h2,
    h3,
    h4 {
        color: #241b28 !important;
        font-weight: 800 !important;
    }

    p,
    label,
    .stMarkdown {
        color: #29232c !important;
    }


    /* ================================
       SIDEBAR
       ================================ */

    [data-testid="stSidebar"] {
        background: #17131b;
    }

    [data-testid="stSidebar"] * {
        color: #f5f2f7 !important;
    }


    /* ================================
       METRICS
       ================================ */

    [data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e7cddd;
        border-radius: 16px;
        padding: 18px;

        box-shadow:
            0 8px 22px
            rgba(90, 35, 75, 0.08);
    }

    [data-testid="stMetricValue"] {
        color: #a31361 !important;
        font-weight: 850 !important;
    }


    /* ================================
       BUTTON
       ================================ */

    .stButton > button {
        border-radius: 12px;
        font-weight: 800;
        min-height: 46px;
    }


    /* ================================
       TABS
       ================================ */

    div[data-baseweb="tab-list"] {
        gap: 8px;
    }

    button[data-baseweb="tab"] {
        font-weight: 800 !important;
        color: #4a3d48 !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #a31361 !important;
    }


    /* ================================
       FILE UPLOADER
       ================================ */

    [data-testid="stFileUploader"] {
        background: #ffffff;
        border: 1px solid #e7cddd;
        border-radius: 14px;
    }


    /* ================================
       FOOTER
       ================================ */

    .footer-text {
        text-align: center;
        color: #6a5b66;
        font-size: 13px;
        padding: 25px 0 5px 0;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 💳 FraudGuard AI")

    st.caption(
        "Credit Card Fraud Detection"
    )

    st.divider()

    if MODEL_PATH:

        st.success("Model detected")

        st.caption(
            f"Model: {MODEL_PATH.name}"
        )

    else:

        st.error("Model not found")

    st.divider()

    st.markdown("### Project")

    st.write("**Model:** XGBoost")

    st.write(
        "**AI Layer:** Agent-based risk decision"
    )

    st.write(
        "**Input:** CSV / Manual"
    )

    st.write(
        "**Output:** Fraud + Risk + Action"
    )


# ============================================================
# MAIN HEADER
# ============================================================

st.title("💳 FraudGuard AI")

st.write(
    "Credit Card Fraud Detection using a trained "
    "XGBoost model with agent-based risk assessment "
    "and business decision support."
)


# ============================================================
# AGENT STATUS
# ============================================================

if agent_load_error:

    st.warning(
        "The fraud agent could not be initialized."
    )

    with st.expander("Technical Status"):

        st.write(
            f"Repository: {BASE_DIR}"
        )

        st.write(
            f"Detected model: {MODEL_PATH}"
        )

        st.code(
            agent_load_error
        )


# ============================================================
# FOUR TABS
# ============================================================

tab_dashboard, tab_detection, tab_agent, tab_about = st.tabs(
    [
        "🏠 Dashboard",
        "🔍 Fraud Detection",
        "🤖 Agentic AI",
        "ℹ️ About Project",
    ]
)


# ============================================================
# DASHBOARD
# ============================================================

with tab_dashboard:

    st.header(
        "Fraud Detection Dashboard"
    )

    st.write(
        "Use the **Fraud Detection** tab to upload "
        "a transaction CSV, select a row, or enter "
        "transaction values manually."
    )

    st.divider()

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Precision",
            "98.73%"
        )

    with c2:
        st.metric(
            "Recall",
            "82.11%"
        )

    with c3:
        st.metric(
            "F1 Score",
            "89.66%"
        )

    with c4:
        st.metric(
            "ROC-AUC",
            "98.35%"
        )

    st.divider()

    st.subheader(
        "System Flow"
    )

    st.write(
        "**Transaction Input → XGBoost Prediction → "
        "Agent Risk Assessment → Business Decision**"
    )

    st.info(
        "The transaction is sent to the trained model "
        "through the existing fraud agent. The agent then "
        "returns the fraud prediction, risk level and "
        "recommended business action."
    )


# ============================================================
# FRAUD DETECTION
# ============================================================

with tab_detection:

    st.header(
        "🔍 Fraud Detection"
    )

    st.write(
        "Provide one transaction and run the trained "
        "FraudGuard AI model."
    )

    st.divider()

    input_mode = st.radio(
        "Input method",
        [
            "📁 Project / Uploaded CSV",
            "✍️ Manual Entry"
        ],
        horizontal=True,
        label_visibility="collapsed"
    )

    transaction = None


    # ========================================================
    # CSV INPUT
    # ========================================================

    if input_mode == "📁 Project / Uploaded CSV":

        project_csvs = sorted(
            list(BASE_DIR.glob("*.csv"))
            + list(BASE_DIR.glob("data/*.csv"))
            + list(BASE_DIR.glob("dataset/*.csv"))
        )

        preferred = [
            p
            for p in project_csvs
            if p.name.lower()
            in {
                "creditcard_small.csv",
                "creditcard.csv",
                "credit_card.csv"
            }
        ]

        csv_choice = None

        if preferred:

            csv_choice = st.selectbox(
                "Choose project CSV",
                preferred,
                format_func=lambda p: p.name
            )

        uploaded = st.file_uploader(
            "Or upload your transaction CSV",
            type=["csv"]
        )

        df = None

        if uploaded is not None:

            try:

                df = pd.read_csv(
                    uploaded
                )

                st.success(
                    f"CSV loaded successfully — "
                    f"{len(df):,} rows"
                )

            except Exception as e:

                st.error(
                    f"Could not read CSV: {e}"
                )

        elif csv_choice is not None:

            try:

                df = pd.read_csv(
                    csv_choice
                )

                st.success(
                    f"Project CSV loaded — "
                    f"{csv_choice.name}"
                )

            except Exception as e:

                st.error(
                    f"Could not read project CSV: {e}"
                )

        else:

            st.info(
                "Upload the transaction CSV here."
            )


        # ====================================================
        # VALIDATE CSV
        # ====================================================

        if df is not None and not df.empty:

            missing_columns = [
                column
                for column in FEATURE_COLUMNS
                if column not in df.columns
            ]

            if missing_columns:

                st.error(
                    "This CSV does not match the trained "
                    "model input."
                )

                st.write(
                    "**Missing columns:**",
                    ", ".join(missing_columns)
                )

                st.caption(
                    "Expected model columns: "
                    + ", ".join(FEATURE_COLUMNS)
                )

            else:

                st.subheader(
                    "1. Select Transaction"
                )

                row_number = st.number_input(
                    "Transaction row",
                    min_value=0,
                    max_value=len(df) - 1,
                    value=0,
                    step=1
                )

                selected_row = df.iloc[
                    int(row_number)
                ].copy()

                transaction = {
                    feature: float(
                        selected_row[feature]
                    )
                    for feature in FEATURE_COLUMNS
                }

                st.dataframe(
                    pd.DataFrame(
                        [transaction]
                    ),
                    width="stretch",
                    hide_index=True
                )

                st.caption(
                    "Only the model features are sent "
                    "for prediction. The Class/target "
                    "column is not sent to the model."
                )


    # ========================================================
    # MANUAL INPUT
    # ========================================================

    else:

        st.subheader(
            "1. Enter Transaction"
        )

        st.caption(
            "Enter the same features used by the trained "
            "XGBoost model."
        )

        values = {}

        with st.form(
            "manual_transaction_form"
        ):

            cols = st.columns(3)

            for index, feature in enumerate(
                FEATURE_COLUMNS
            ):

                with cols[index % 3]:

                    values[feature] = st.number_input(
                        feature,
                        value=0.0,
                        format="%.8f"
                    )

            submitted = st.form_submit_button(
                "Use These Values",
                type="primary",
                width="stretch"
            )

        if submitted:

            transaction = values

            st.success(
                "Manual transaction prepared successfully."
            )


    # ========================================================
    # PREDICTION
    # ========================================================

    st.divider()

    st.subheader(
        "2. Run Fraud Detection"
    )

    run_prediction = st.button(
        "🚀 Predict Fraud Risk",
        type="primary",
        width="stretch"
    )


    if run_prediction:

        if transaction is None:

            st.error(
                "Please provide a CSV transaction "
                "or enter the values manually."
            )

        elif fraud_detection_agent is None:

            st.error(
                "Fraud agent is not available."
            )

            st.info(
                "Please verify that the trained model "
                "and agent.py/tools.py are committed "
                "to the GitHub repository."
            )

        else:

            try:

                clean_transaction = {
                    column: float(
                        transaction[column]
                    )
                    for column in FEATURE_COLUMNS
                }

                with st.spinner(
                    "FraudGuard AI is analyzing..."
                ):

                    result = fraud_detection_agent(
                        clean_transaction
                    )


                # =================================================
                # AGENT RESULT
                # =================================================

                fraud_probability = float(
                    result["fraud_probability"]
                )

                prediction = int(
                    result["prediction"]
                )

                risk_level = str(
                    result["risk_level"]
                ).upper()

                action = str(
                    result["recommended_action"]
                ).upper()


                # =================================================
                # OUTPUT
                # =================================================

                st.divider()

                st.subheader(
                    "3. Prediction Result"
                )

                r1, r2, r3 = st.columns(3)

                with r1:

                    st.metric(
                        "Fraud Probability",
                        f"{fraud_probability * 100:.2f}%"
                    )

                with r2:

                    st.metric(
                        "ML Prediction",
                        (
                            "FRAUDULENT"
                            if prediction == 1
                            else "GENUINE"
                        )
                    )

                with r3:

                    st.metric(
                        "Recommended Action",
                        action
                    )


                st.progress(
                    min(
                        max(
                            fraud_probability,
                            0.0
                        ),
                        1.0
                    ),
                    text=(
                        f"Fraud Probability: "
                        f"{fraud_probability * 100:.2f}%"
                    )
                )


                # =================================================
                # RISK
                # =================================================

                if risk_level == "HIGH":

                    st.error(
                        f"🔴 HIGH RISK — {action}"
                    )

                elif risk_level == "MEDIUM":

                    st.warning(
                        f"🟠 MEDIUM RISK — {action}"
                    )

                else:

                    st.success(
                        f"🟢 LOW RISK — {action}"
                    )


                # =================================================
                # FINAL AGENT OUTPUT
                # =================================================

                st.divider()

                st.subheader(
                    "Agent Output"
                )

                st.write(
                    f"**ML Prediction:** "
                    f"{'FRAUDULENT' if prediction == 1 else 'GENUINE'}"
                )

                st.write(
                    f"**Fraud Probability:** "
                    f"{fraud_probability * 100:.2f}%"
                )

                st.write(
                    f"**Risk Level:** "
                    f"{risk_level}"
                )

                st.write(
                    f"**Recommended Action:** "
                    f"{action}"
                )


            except Exception as e:

                st.error(
                    "Prediction failed."
                )

                st.exception(e)


# ============================================================
# AGENTIC AI
# ============================================================

with tab_agent:

    st.header(
        "🤖 Agentic AI"
    )

    st.write(
        "FraudGuard AI uses the existing agent workflow "
        "from the repository."
    )

    st.divider()

    st.subheader(
        "Agent Workflow"
    )

    st.write(
        "**Transaction → Fraud Prediction → "
        "Risk Assessment → Business Decision**"
    )

    st.divider()

    st.subheader(
        "Agent Output"
    )

    st.write(
        "• Fraud probability"
    )

    st.write(
        "• Fraud / genuine prediction"
    )

    st.write(
        "• Risk level"
    )

    st.write(
        "• Recommended action"
    )

    st.divider()

    if MODEL_PATH:

        st.success(
            f"Trained model detected: "
            f"{MODEL_PATH.name}"
        )

    else:

        st.error(
            "No trained fraud model detected."
        )


# ============================================================
# ABOUT PROJECT
# ============================================================

with tab_about:

    st.header(
        "ℹ️ About Project"
    )

    st.write(
        "**Project:** Credit Card Fraud Detection"
    )

    st.write(
        "**Machine Learning Model:** XGBoost"
    )

    st.write(
        "**Application:** Streamlit"
    )

    st.write(
        "**AI Layer:** Tool-based Agentic AI"
    )

    st.write(
        "**Developer:** Devadharshini Murugan"
    )

    st.divider()

    st.subheader(
        "Model Performance"
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Precision",
            "98.73%"
        )

    with c2:
        st.metric(
            "Recall",
            "82.11%"
        )

    with c3:
        st.metric(
            "F1 Score",
            "89.66%"
        )

    with c4:
        st.metric(
            "ROC-AUC",
            "98.35%"
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer-text">
        FraudGuard AI • Built by Devadharshini Murugan
    </div>
    """,
    unsafe_allow_html=True
)
