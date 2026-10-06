import streamlit as st
import pandas as pd
from pathlib import Path


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="FraudGuard AI",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

/* =========================================================
   GLOBAL
========================================================= */

.stApp {
    background: linear-gradient(
        135deg,
        #fff7fb 0%,
        #ffeaf4 50%,
        #f8efff 100%
    );
}

.main .block-container {
    max-width: 1250px;
    padding-top: 25px;
    padding-bottom: 50px;
}

html, body, [class*="css"] {
    color: #171717 !important;
}

p, label, span {
    color: #242424;
}

h1, h2, h3, h4 {
    color: #181818 !important;
    font-weight: 800 !important;
}


/* =========================================================
   TOP HEADER
========================================================= */

.main-header {
    background: linear-gradient(
        135deg,
        #9c145d,
        #d51d76,
        #7d2bb4
    );

    border-radius: 24px;

    padding: 30px 36px;

    margin-bottom: 22px;

    box-shadow:
        0 15px 35px rgba(130, 25, 100, 0.20);
}

.main-title {
    color: white !important;
    font-size: 38px;
    font-weight: 900;
    margin: 0;
}

.main-subtitle {
    color: rgba(255,255,255,0.94) !important;
    font-size: 16px;
    margin-top: 6px;
}


/* =========================================================
   TOP NAVIGATION
========================================================= */

div[data-testid="stTabs"] button {
    color: #5a1640 !important;
    font-weight: 800 !important;
    font-size: 15px !important;
}

div[data-testid="stTabs"] button[aria-selected="true"] {
    color: #a91562 !important;
}


/* =========================================================
   SECTION TITLE
========================================================= */

.section-title {
    color: #94165a !important;
    font-size: 29px;
    font-weight: 900;
    margin-top: 10px;
    margin-bottom: 7px;
}

.section-subtitle {
    color: #444444 !important;
    font-size: 15px;
    line-height: 1.6;
    margin-bottom: 22px;
}


/* =========================================================
   WHITE CONTAINER
========================================================= */

.white-card {
    background: rgba(255,255,255,0.97);

    border: 1px solid #efc5da;

    border-radius: 20px;

    padding: 24px;

    box-shadow:
        0 8px 24px rgba(120,30,90,0.08);

    margin-bottom: 20px;
}

.card-title {
    color: #8f1858 !important;
    font-size: 21px;
    font-weight: 900;
    margin-bottom: 8px;
}

.card-text {
    color: #404040 !important;
    font-size: 14px;
    line-height: 1.65;
}


/* =========================================================
   INPUT AREA
========================================================= */

.input-container {
    background: white;

    border: 2px solid #e9bfd5;

    border-radius: 20px;

    padding: 25px;

    box-shadow:
        0 8px 25px rgba(120,30,90,0.08);

    margin-top: 15px;
    margin-bottom: 20px;
}

.input-heading {
    color: #8f1858 !important;
    font-size: 23px;
    font-weight: 900;
    margin-bottom: 5px;
}

.input-help {
    color: #555555 !important;
    font-size: 14px;
    margin-bottom: 15px;
}


/* =========================================================
   SELECTED TRANSACTION
========================================================= */

.transaction-header {
    background: #fff3f8;

    border-left: 5px solid #c81769;

    border-radius: 10px;

    padding: 13px 16px;

    color: #7f124e !important;

    font-weight: 900;

    margin-top: 18px;
    margin-bottom: 10px;
}


/* =========================================================
   RESULT CONTAINER
========================================================= */

.result-container {
    background: white;

    border: 2px solid #dba9c7;

    border-radius: 22px;

    padding: 28px;

    margin-top: 25px;

    box-shadow:
        0 12px 32px rgba(120,30,90,0.12);
}

.result-heading {
    color: #8f1858 !important;

    font-size: 26px;

    font-weight: 900;

    margin-bottom: 20px;
}


/* =========================================================
   RESULT CARDS
========================================================= */

.result-card {
    background: #fff9fc;

    border: 1px solid #edc8da;

    border-radius: 16px;

    padding: 20px;

    text-align: center;

    min-height: 130px;

    display: flex;

    flex-direction: column;

    justify-content: center;
}

.result-label {
    color: #555555 !important;

    font-size: 12px;

    font-weight: 800;

    text-transform: uppercase;

    letter-spacing: 0.6px;

    margin-bottom: 8px;
}

.result-value {
    color: #97155c !important;

    font-size: 26px;

    font-weight: 950;
}


/* =========================================================
   RISK BOX
========================================================= */

.risk-box {
    margin-top: 20px;

    border-radius: 17px;

    padding: 20px;

    text-align: center;
}

.risk-title {
    font-size: 13px;

    font-weight: 800;

    color: #444444 !important;

    text-transform: uppercase;
}

.risk-value {
    font-size: 30px;

    font-weight: 950;

    margin-top: 5px;
}


/* =========================================================
   PROGRESS
========================================================= */

.progress-title {
    color: #444444 !important;

    font-size: 14px;

    font-weight: 800;

    margin-top: 20px;

    margin-bottom: 5px;
}


/* =========================================================
   BUTTON
========================================================= */

.stButton > button {
    background: linear-gradient(
        90deg,
        #c81769,
        #8d28bd
    ) !important;

    color: white !important;

    border: none !important;

    border-radius: 12px !important;

    font-size: 16px !important;

    font-weight: 900 !important;

    padding: 12px 20px !important;

    min-height: 48px;

    box-shadow:
        0 8px 20px rgba(140,30,110,0.22);
}

.stButton > button:hover {
    background: linear-gradient(
        90deg,
        #a91459,
        #70229b
    ) !important;

    color: white !important;
}


/* =========================================================
   FILE UPLOADER
========================================================= */

[data-testid="stFileUploader"] {
    background: #fffafd;

    border: 1px solid #e8bfd4;

    border-radius: 14px;

    padding: 10px;
}


/* =========================================================
   DATAFRAME
========================================================= */

[data-testid="stDataFrame"] {
    border: 1px solid #e8bfd4;

    border-radius: 12px;
}


/* =========================================================
   FOOTER
========================================================= */

.footer {
    text-align: center;

    color: #555555 !important;

    font-size: 13px;

    margin-top: 45px;

    padding-top: 20px;

    border-top: 1px solid #e8c5d7;
}


/* =========================================================
   HIDE STREAMLIT SIDEBAR
========================================================= */

section[data-testid="stSidebar"] {
    display: none;
}

button[kind="header"] {
    display: none;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="main-header">

    <div class="main-title">
        💳 FraudGuard AI
    </div>

    <div class="main-subtitle">
        Credit Card Fraud Detection using Machine Learning
        and Agentic AI Risk Decision Support
    </div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# FOUR TOP TABS
# ============================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "🏠 Dashboard",
    "🔍 Fraud Detection",
    "🤖 Agentic AI",
    "ℹ️ About Project"
])


# ============================================================
# TAB 1 — DASHBOARD
# ============================================================

with tab1:

    st.markdown(
        '<div class="section-title">FraudGuard AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-subtitle">
            A credit-card fraud detection application that takes
            transaction data, generates an ML fraud prediction,
            and passes the result through an agentic risk-decision layer.
        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown("""
    <div class="white-card">

        <div class="card-title">
            How to Use the Application
        </div>

        <div class="card-text">

            <b>Step 1:</b> Open <b>Fraud Detection</b>.<br><br>

            <b>Step 2:</b> Upload your transaction CSV file.<br><br>

            <b>Step 3:</b> Select the transaction row that you want
            to test.<br><br>

            <b>Step 4:</b> Click <b>Run FraudGuard AI</b>.<br><br>

            <b>Step 5:</b> The application sends the transaction
            through the trained ML model and Agentic AI layer.<br><br>

            <b>Step 6:</b> The final result shows fraud probability,
            prediction, risk level and recommended action.

        </div>

    </div>
    """, unsafe_allow_html=True)


    st.markdown(
        '<div class="section-title">System Flow</div>',
        unsafe_allow_html=True
    )


    flow1, flow2, flow3, flow4 = st.columns(4)


    with flow1:

        st.markdown("""
        <div class="white-card" style="text-align:center;">

            <div style="font-size:32px;">📄</div>

            <div class="card-title">
                CSV Input
            </div>

            <div class="card-text">
                Transaction data is uploaded.
            </div>

        </div>
        """, unsafe_allow_html=True)


    with flow2:

        st.markdown("""
        <div class="white-card" style="text-align:center;">

            <div style="font-size:32px;">🧠</div>

            <div class="card-title">
                ML Prediction
            </div>

            <div class="card-text">
                XGBoost predicts fraud probability.
            </div>

        </div>
        """, unsafe_allow_html=True)


    with flow3:

        st.markdown("""
        <div class="white-card" style="text-align:center;">

            <div style="font-size:32px;">🤖</div>

            <div class="card-title">
                Agent
            </div>

            <div class="card-text">
                The agent assesses transaction risk.
            </div>

        </div>
        """, unsafe_allow_html=True)


    with flow4:

        st.markdown("""
        <div class="white-card" style="text-align:center;">

            <div style="font-size:32px;">🚦</div>

            <div class="card-title">
                Decision
            </div>

            <div class="card-text">
                Approve, Review or Block.
            </div>

        </div>
        """, unsafe_allow_html=True)


# ============================================================
# TAB 2 — FRAUD DETECTION
# ============================================================

with tab2:

    st.markdown(
        '<div class="section-title">🔍 Fraud Detection</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-subtitle">
            Upload your CSV, select one transaction, and run the
            FraudGuard AI prediction.
        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # INPUT
    # --------------------------------------------------------

    st.markdown("""
    <div class="input-container">

        <div class="input-heading">
            1. Transaction Input
        </div>

        <div class="input-help">
            Upload the CSV containing the transaction records.
        </div>

    </div>
    """, unsafe_allow_html=True)


    uploaded_file = st.file_uploader(
        "Upload Transaction CSV",
        type=["csv"],
        key="fraud_csv"
    )


    if uploaded_file is not None:

        try:

            df = pd.read_csv(uploaded_file)

            st.success(
                f"CSV loaded successfully — {len(df):,} transactions found."
            )


            # ------------------------------------------------
            # REQUIRED FEATURES
            # ------------------------------------------------

            required_features = [
                "Time",
                "V1", "V2", "V3", "V4", "V5", "V6", "V7",
                "V8", "V9", "V10", "V11", "V12", "V13", "V14",
                "V15", "V16", "V17", "V18", "V19", "V20", "V21",
                "V22", "V23", "V24", "V25", "V26", "V27", "V28",
                "Amount"
            ]


            missing = [
                c for c in required_features
                if c not in df.columns
            ]


            if missing:

                st.error(
                    "The uploaded CSV does not contain all required "
                    "transaction features."
                )

                st.write("Missing columns:")

                st.code(", ".join(missing))

                st.stop()


            # ------------------------------------------------
            # TRANSACTION SELECTION
            # ------------------------------------------------

            st.markdown("""
            <div class="transaction-header">
                2. Select Transaction
            </div>
            """, unsafe_allow_html=True)


            row_number = st.number_input(
                "Transaction row",
                min_value=0,
                max_value=len(df) - 1,
                value=0,
                step=1,
                help="Select the row that you want the AI system to analyze."
            )


            selected_row = df.iloc[int(row_number)]


            st.caption(
                f"Selected transaction: Row {int(row_number)}"
            )


            # ------------------------------------------------
            # INPUT PREVIEW
            # ------------------------------------------------

            with st.expander(
                "👁️ View selected transaction input",
                expanded=True
            ):

                input_df = pd.DataFrame(
                    [selected_row[required_features]]
                )

                st.dataframe(
                    input_df,
                    width="stretch",
                    hide_index=True
                )


            # ------------------------------------------------
            # RUN BUTTON
            # ------------------------------------------------

            st.markdown("""
            <div class="transaction-header">
                3. Run FraudGuard AI
            </div>
            """, unsafe_allow_html=True)


            run_button = st.button(
                "🚀 Run FraudGuard AI",
                type="primary",
                width="stretch",
                key="run_fraud"
            )


            if run_button:

                # Import only when required.
                # This prevents the whole UI from crashing
                # before the user uploads a transaction.

                try:

                    from agent import fraud_detection_agent

                except Exception as e:

                    st.error(
                        "The Agent could not be loaded."
                    )

                    st.code(str(e))

                    st.stop()


                transaction = (
                    selected_row[required_features]
                    .to_dict()
                )


                # ------------------------------------------------
                # AGENT EXECUTION
                # ------------------------------------------------

                try:

                    with st.spinner(
                        "FraudGuard AI is analyzing the transaction..."
                    ):

                        result = fraud_detection_agent(
                            transaction
                        )


                except Exception as e:

                    st.error(
                        "Fraud detection failed."
                    )

                    st.code(str(e))

                    st.stop()


                # ------------------------------------------------
                # GET RESULT
                # ------------------------------------------------

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


                prediction_text = (
                    "FRAUDULENT"
                    if prediction == 1
                    else "GENUINE"
                )


                # =================================================
                # RESULT — EVERYTHING INSIDE ONE BOX
                # =================================================

                st.markdown(
                    '<div class="result-container">',
                    unsafe_allow_html=True
                )


                st.markdown(
                    '<div class="result-heading">'
                    '✅ FraudGuard AI Result'
                    '</div>',
                    unsafe_allow_html=True
                )


                # ------------------------------------------------
                # RESULT CARDS
                # ------------------------------------------------

                r1, r2, r3 = st.columns(3)


                with r1:

                    st.markdown(f"""
                    <div class="result-card">

                        <div class="result-label">
                            Fraud Probability
                        </div>

                        <div class="result-value">
                            {fraud_probability * 100:.2f}%
                        </div>

                    </div>
                    """, unsafe_allow_html=True)


                with r2:

                    st.markdown(f"""
                    <div class="result-card">

                        <div class="result-label">
                            ML Prediction
                        </div>

                        <div class="result-value">
                            {prediction_text}
                        </div>

                    </div>
                    """, unsafe_allow_html=True)


                with r3:

                    st.markdown(f"""
                    <div class="result-card">

                        <div class="result-label">
                            Agent Decision
                        </div>

                        <div class="result-value">
                            {action}
                        </div>

                    </div>
                    """, unsafe_allow_html=True)


                # ------------------------------------------------
                # RISK
                # ------------------------------------------------

                if risk_level == "HIGH":

                    risk_bg = "#fff0f0"
                    risk_border = "#dc4b4b"
                    risk_color = "#b42323"

                    risk_icon = "🔴"

                elif risk_level == "MEDIUM":

                    risk_bg = "#fff8e8"
                    risk_border = "#e2a52c"
                    risk_color = "#9a6500"

                    risk_icon = "🟠"

                else:

                    risk_bg = "#eefaf1"
                    risk_border = "#49a866"
                    risk_color = "#24733b"

                    risk_icon = "🟢"


                st.markdown(f"""
                <div class="risk-box"
                     style="
                        background:{risk_bg};
                        border:2px solid {risk_border};
                     ">

                    <div class="risk-title">
                        Risk Level
                    </div>

                    <div class="risk-value"
                         style="color:{risk_color} !important;">

                        {risk_icon} {risk_level}

                    </div>

                </div>
                """, unsafe_allow_html=True)


                # ------------------------------------------------
                # PROBABILITY BAR
                # ------------------------------------------------

                st.markdown(
                    f"""
                    <div class="progress-title">
                        Fraud Probability: {fraud_probability * 100:.2f}%
                    </div>
                    """,
                    unsafe_allow_html=True
                )


                st.progress(
                    min(
                        max(fraud_probability, 0.0),
                        1.0
                    )
                )


                # ------------------------------------------------
                # FINAL DECISION
                # ------------------------------------------------

                st.markdown(f"""
                <div style="
                    margin-top:20px;
                    padding:16px;
                    background:#f8f1f6;
                    border-radius:13px;
                    text-align:center;
                ">

                    <div style="
                        color:#555555;
                        font-size:12px;
                        font-weight:800;
                        text-transform:uppercase;
                    ">
                        Final Agent Recommendation
                    </div>

                    <div style="
                        color:#8f1858;
                        font-size:24px;
                        font-weight:950;
                        margin-top:5px;
                    ">
                        {action}
                    </div>

                </div>
                """, unsafe_allow_html=True)


                st.markdown(
                    '</div>',
                    unsafe_allow_html=True
                )


        except Exception as e:

            st.error(
                f"Unable to process the CSV: {e}"
            )


    else:

        st.info(
            "Please upload your transaction CSV to begin."
        )


# ============================================================
# TAB 3 — AGENTIC AI
# ============================================================

with tab3:

    st.markdown(
        '<div class="section-title">🤖 Agentic AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-subtitle">
            The agent receives the ML prediction and converts it into
            a practical risk-based decision.
        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown("""
    <div class="white-card">

        <div class="card-title">
            Agent Decision Flow
        </div>

        <div class="card-text"
             style="font-size:18px; font-weight:800;">

            Transaction
            &nbsp; → &nbsp;
            XGBoost Prediction
            &nbsp; → &nbsp;
            Risk Assessment
            &nbsp; → &nbsp;
            Final Decision

        </div>

    </div>
    """, unsafe_allow_html=True)


    a1, a2, a3 = st.columns(3)


    with a1:

        st.markdown("""
        <div class="white-card">

            <div class="card-title">
                1. ML Prediction
            </div>

            <div class="card-text">
                The trained XGBoost model analyzes the transaction
                features and produces a fraud probability.
            </div>

        </div>
        """, unsafe_allow_html=True)


    with a2:

        st.markdown("""
        <div class="white-card">

            <div class="card-title">
                2. Risk Assessment
            </div>

            <div class="card-text">
                The agent interprets the fraud probability and
                determines the transaction risk level.
            </div>

        </div>
        """, unsafe_allow_html=True)


    with a3:

        st.markdown("""
        <div class="white-card">

            <div class="card-title">
                3. Business Decision
            </div>

            <div class="card-text">
                The agent converts the risk assessment into
                APPROVE, REVIEW or BLOCK.
            </div>

        </div>
        """, unsafe_allow_html=True)


# ============================================================
# TAB 4 — ABOUT PROJECT
# ============================================================

with tab4:

    st.markdown(
        '<div class="section-title">ℹ️ About Project</div>',
        unsafe_allow_html=True
    )


    c1, c2 = st.columns(2)


    with c1:

        st.markdown("""
        <div class="white-card">

            <div class="card-title">
                Project Information
            </div>

            <div class="card-text">

                <b>Project:</b>
                Credit Card Fraud Detection<br><br>

                <b>Machine Learning Model:</b>
                XGBoost<br><br>

                <b>Application:</b>
                Streamlit<br><br>

                <b>AI Layer:</b>
                Agentic AI<br><br>

                <b>Developer:</b>
                Devadharshini Murugan

            </div>

        </div>
        """, unsafe_allow_html=True)


    with c2:

        st.markdown("""
        <div class="white-card">

            <div class="card-title">
                Dataset
            </div>

            <div class="card-text">

                The application works with credit-card transaction
                records containing the transaction time,
                PCA-transformed features V1–V28 and transaction amount.

                <br><br>

                The target <b>Class</b> column, when present in the
                uploaded CSV, is not passed to the prediction model.

            </div>

        </div>
        """, unsafe_allow_html=True)


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">

    FraudGuard AI • Credit Card Fraud Detection & Agentic Risk Decision System

    <br><br>

    Built by <b>Devadharshini Murugan</b>

</div>
""", unsafe_allow_html=True)
