import streamlit as st
import pandas as pd

from agent import fraud_detection_agent


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="FraudGuard AI",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

    /* ---------- GLOBAL ---------- */

    .stApp {
        background: linear-gradient(
            135deg,
            #fff7fb 0%,
            #ffeaf4 50%,
            #f8efff 100%
        );
    }

    html, body, [class*="css"] {
        color: #171717 !important;
    }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1250px;
    }

    p, li, label, span, div {
        color: #202020;
    }

    h1, h2, h3, h4 {
        color: #171717 !important;
        font-weight: 800 !important;
    }


    /* ---------- SIDEBAR ---------- */

    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #fffafd 0%,
            #ffeef7 100%
        );
        border-right: 1px solid #f3c6da;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label {
        color: #222222 !important;
    }

    .sidebar-title {
        font-size: 25px;
        font-weight: 800;
        color: #9d175b;
        margin-bottom: 3px;
    }

    .sidebar-subtitle {
        font-size: 13px;
        color: #555555;
        margin-bottom: 25px;
    }


    /* ---------- CREDIT CARD ---------- */

    .credit-card {
        width: 100%;
        height: 185px;
        border-radius: 22px;
        padding: 24px;
        margin-bottom: 25px;

        background: linear-gradient(
            135deg,
            #8e155c 0%,
            #d71973 48%,
            #8b2bc3 100%
        );

        box-shadow:
            0 15px 35px rgba(155, 20, 95, 0.25);

        position: relative;
        overflow: hidden;
    }

    .credit-card::before {
        content: "";
        position: absolute;
        width: 170px;
        height: 170px;
        border-radius: 50%;
        background: rgba(255,255,255,0.08);
        right: -60px;
        top: -70px;
    }

    .credit-card::after {
        content: "";
        position: absolute;
        width: 130px;
        height: 130px;
        border-radius: 50%;
        background: rgba(255,255,255,0.06);
        left: -60px;
        bottom: -70px;
    }

    .card-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: relative;
        z-index: 2;
    }

    .card-brand {
        color: white !important;
        font-size: 21px;
        font-weight: 800;
        letter-spacing: 0.5px;
    }

    .card-chip {
        width: 42px;
        height: 30px;
        border-radius: 7px;
        background: linear-gradient(
            135deg,
            #ffe7a8,
            #dcae53
        );
        border: 1px solid rgba(255,255,255,0.4);
    }

    .card-number {
        color: white !important;
        font-size: 19px;
        letter-spacing: 3px;
        margin-top: 30px;
        position: relative;
        z-index: 2;
    }

    .card-bottom {
        display: flex;
        justify-content: space-between;
        margin-top: 17px;
        position: relative;
        z-index: 2;
    }

    .card-label {
        color: rgba(255,255,255,0.72) !important;
        font-size: 9px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .card-value {
        color: white !important;
        font-size: 12px;
        font-weight: 700;
    }


    /* ---------- HERO ---------- */

    .hero {
        background: linear-gradient(
            135deg,
            #c81769,
            #9c1c8f,
            #7024b7
        );

        border-radius: 26px;
        padding: 38px 42px;
        margin-bottom: 30px;

        box-shadow:
            0 18px 40px rgba(139, 30, 130, 0.22);
    }

    .hero h1 {
        color: white !important;
        font-size: 42px;
        margin-bottom: 8px;
    }

    .hero p {
        color: rgba(255,255,255,0.94) !important;
        font-size: 17px;
        line-height: 1.6;
        margin-bottom: 0;
    }


    /* ---------- SECTION ---------- */

    .section-title {
        font-size: 30px;
        color: #8f1858 !important;
        margin-top: 15px;
        margin-bottom: 8px;
    }

    .section-text {
        color: #3f3f3f !important;
        font-size: 16px;
        line-height: 1.7;
    }


    /* ---------- WHITE CARDS ---------- */

    .info-card {
        background: rgba(255,255,255,0.94);
        border: 1px solid #f1c9dc;
        border-radius: 20px;
        padding: 25px;
        height: 100%;

        box-shadow:
            0 10px 25px rgba(150, 50, 100, 0.08);
    }

    .info-card h3 {
        color: #8e1858 !important;
        font-size: 20px;
        margin-bottom: 10px;
    }

    .info-card p {
        color: #3b3b3b !important;
        line-height: 1.65;
    }

    .info-card strong {
        color: #171717 !important;
    }


    /* ---------- WORKFLOW ---------- */

    .workflow-box {
        background: white;
        border: 1px solid #efc6da;
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        min-height: 165px;

        box-shadow: 0 10px 25px rgba(120,30,90,0.08);
    }

    .workflow-icon {
        font-size: 35px;
        margin-bottom: 8px;
    }

    .workflow-title {
        font-size: 18px;
        font-weight: 800;
        color: #222222 !important;
    }

    .workflow-text {
        font-size: 14px;
        color: #555555 !important;
        line-height: 1.5;
    }


    /* ---------- METRIC CARDS ---------- */

    .metric-card {
        background: white;
        border-radius: 18px;
        padding: 20px;
        text-align: center;
        border: 1px solid #efc9dc;

        box-shadow: 0 8px 20px rgba(120,30,90,0.07);
    }

    .metric-number {
        font-size: 28px;
        font-weight: 800;
        color: #b31368 !important;
    }

    .metric-label {
        font-size: 13px;
        color: #555555 !important;
        margin-top: 4px;
    }


    /* ---------- INPUT AREA ---------- */

    .input-box {
        background: white;
        border: 1px solid #efc6da;
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 10px 25px rgba(120,30,90,0.07);
        margin-bottom: 20px;
    }

    .input-title {
        color: #8f1858 !important;
        font-size: 22px;
        font-weight: 800;
        margin-bottom: 6px;
    }

    .input-description {
        color: #555555 !important;
        font-size: 14px;
        margin-bottom: 18px;
    }


    /* ---------- RESULT BOX ---------- */

    .result-box {
        background: white;
        border-radius: 22px;
        border: 2px solid #e6c5d8;
        padding: 28px;
        margin-top: 20px;

        box-shadow: 0 12px 30px rgba(120,30,90,0.10);
    }

    .result-title {
        color: #8f1858 !important;
        font-size: 25px;
        font-weight: 800;
    }

    .result-value {
        font-size: 34px;
        font-weight: 900;
        color: #191919 !important;
    }


    /* ---------- RISK BOXES ---------- */

    .risk-high {
        background: #fff0f0;
        border: 2px solid #e14a4a;
        border-radius: 16px;
        padding: 18px;
        text-align: center;
    }

    .risk-medium {
        background: #fff8e8;
        border: 2px solid #e5a927;
        border-radius: 16px;
        padding: 18px;
        text-align: center;
    }

    .risk-low {
        background: #effaf2;
        border: 2px solid #46a866;
        border-radius: 16px;
        padding: 18px;
        text-align: center;
    }

    .risk-label {
        font-size: 13px;
        color: #444444 !important;
    }

    .risk-value {
        font-size: 28px;
        font-weight: 900;
        color: #171717 !important;
    }


    /* ---------- BUTTON ---------- */

    .stButton > button {
        width: 100%;
        border-radius: 12px;
        border: none;
        padding: 12px 20px;

        background: linear-gradient(
            90deg,
            #c81769,
            #8d28bd
        );

        color: white !important;
        font-weight: 800;
        font-size: 16px;

        box-shadow: 0 8px 18px rgba(150,30,110,0.20);
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 10px 22px rgba(150,30,110,0.28);
    }


    /* ---------- FILE UPLOADER ---------- */

    [data-testid="stFileUploader"] {
        background: white;
        border-radius: 14px;
        padding: 10px;
        border: 1px solid #efc6da;
    }


    /* ---------- EXPANDER ---------- */

    .streamlit-expanderHeader {
        color: #222222 !important;
        font-weight: 700 !important;
    }


    /* ---------- FOOTER ---------- */

    .footer {
        text-align: center;
        padding: 30px 0 10px 0;
        color: #555555 !important;
        font-size: 13px;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("""
    <div class="credit-card">

        <div class="card-top">
            <div class="card-brand">FraudGuard AI</div>
            <div class="card-chip"></div>
        </div>

        <div class="card-number">
            ••••  ••••  ••••  2026
        </div>

        <div class="card-bottom">
            <div>
                <div class="card-label">SYSTEM</div>
                <div class="card-value">FRAUD DETECTION</div>
            </div>

            <div>
                <div class="card-label">AI</div>
                <div class="card-value">ACTIVE</div>
            </div>
        </div>

    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="sidebar-title">Navigation</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-subtitle">FraudGuard AI Control Panel</div>',
        unsafe_allow_html=True
    )

    page = st.radio(
        "Go to",
        [
            "🏠 Dashboard",
            "🔍 Fraud Detection",
            "🤖 Agentic AI",
            "ℹ️ About Project"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")

    st.markdown("""
    <div style="
        background:white;
        border:1px solid #efc6da;
        border-radius:15px;
        padding:15px;
    ">
        <b style="color:#8f1858;">Project Owner</b><br>
        <span style="color:#333333;">Devadharshini Murugan</span>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# DASHBOARD
# =========================================================

if page == "🏠 Dashboard":

    st.markdown("""
    <div class="hero">

        <h1>💳 FraudGuard AI</h1>

        <p>
            Intelligent Credit Card Fraud Detection &
            Agentic Risk Decision System
        </p>

        <p style="margin-top:12px;">
            Built by <b>Devadharshini Murugan</b>
        </p>

    </div>
    """, unsafe_allow_html=True)


    st.markdown(
        '<div class="section-title">🛡️ Intelligent Fraud Protection</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="section-text">
        FraudGuard AI analyzes credit card transactions using a trained
        XGBoost Machine Learning model and then uses an agentic decision
        workflow to assess risk and recommend a business action.
    </div>
    """, unsafe_allow_html=True)

    st.write("")


    # Workflow
    st.markdown(
        '<div class="section-title">⚙️ How the System Works</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown("""
        <div class="workflow-box">
            <div class="workflow-icon">💳</div>
            <div class="workflow-title">1. Transaction</div>
            <div class="workflow-text">
                Transaction details are provided as input.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="workflow-box">
            <div class="workflow-icon">🧠</div>
            <div class="workflow-title">2. ML Prediction</div>
            <div class="workflow-text">
                XGBoost predicts the probability of fraud.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="workflow-box">
            <div class="workflow-icon">🎯</div>
            <div class="workflow-title">3. Risk Assessment</div>
            <div class="workflow-text">
                The agent converts probability into a risk level.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown("""
        <div class="workflow-box">
            <div class="workflow-icon">🚦</div>
            <div class="workflow-title">4. Decision</div>
            <div class="workflow-text">
                The system recommends Approve, Review or Block.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")


    # Metrics
    st.markdown(
        '<div class="section-title">📊 Model Performance</div>',
        unsafe_allow_html=True
    )

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-number">98.73%</div>
            <div class="metric-label">Precision</div>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-number">82.11%</div>
            <div class="metric-label">Recall</div>
        </div>
        """, unsafe_allow_html=True)

    with m3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-number">89.66%</div>
            <div class="metric-label">F1 Score</div>
        </div>
        """, unsafe_allow_html=True)

    with m4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-number">98.35%</div>
            <div class="metric-label">ROC-AUC</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    st.markdown("""
    <div class="info-card">

        <h3>🚀 Project Objective</h3>

        <p>
            The objective of this project is to identify potentially
            fraudulent credit card transactions while reducing
            unnecessary false alerts on genuine transactions.
        </p>

        <p>
            Because fraud transactions are highly imbalanced compared
            with genuine transactions, Precision, Recall, F1 Score and
            ROC-AUC are used instead of relying only on accuracy.
        </p>

    </div>
    """, unsafe_allow_html=True)


# =========================================================
# FRAUD DETECTION
# =========================================================

elif page == "🔍 Fraud Detection":

    st.markdown(
        '<div class="section-title">🔍 Fraud Detection</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="section-text">
        Enter a transaction below and run the FraudGuard AI agent.
        The system will generate a fraud probability, risk level and
        recommended action.
    </div>
    """, unsafe_allow_html=True)

    st.write("")


    # -----------------------------------------------------
    # INPUT METHOD
    # -----------------------------------------------------

    st.markdown("""
    <div class="input-box">

        <div class="input-title">1️⃣ Provide Transaction Input</div>

        <div class="input-description">
            You can either enter a transaction manually or load a
            transaction from the project dataset.
        </div>

    </div>
    """, unsafe_allow_html=True)


    input_method = st.radio(
        "Choose input method",
        ["Use Demo Transaction", "Enter Transaction Manually"],
        horizontal=True
    )


    transaction = None


    # -----------------------------------------------------
    # DEMO TRANSACTION
    # -----------------------------------------------------

    if input_method == "Use Demo Transaction":

        try:

            demo_df = pd.read_csv("creditcard_small.csv")

            demo_index = st.number_input(
                "Select dataset row",
                min_value=0,
                max_value=len(demo_df) - 1,
                value=0,
                step=1
            )

            selected_row = demo_df.iloc[int(demo_index)]

            transaction = selected_row.drop("Class").to_dict()

            st.success(
                "Demo transaction loaded successfully. "
                "Click **Run FraudGuard AI** below to predict it."
            )

            with st.expander("👁️ View transaction input"):

                display_df = pd.DataFrame([transaction])

                st.dataframe(
                    display_df,
                    use_container_width=True
                )

        except Exception as e:

            st.error(
                f"Could not load the dataset: {e}"
            )


    # -----------------------------------------------------
    # MANUAL INPUT
    # -----------------------------------------------------

    else:

        st.markdown("""
        <div class="info-card">

            <h3>📝 Transaction Features</h3>

            <p>
                Enter values for the transaction features used by the
                trained XGBoost model.
            </p>

        </div>
        """, unsafe_allow_html=True)

        st.write("")


        # Default values
        time_value = st.number_input(
            "Time",
            value=0.0,
            help="Transaction time value from the dataset."
        )

        amount_value = st.number_input(
            "Amount",
            min_value=0.0,
            value=100.0,
            help="Transaction amount."
        )


        st.markdown("### 🔢 PCA Transaction Features")

        v_values = {}

        columns = [f"V{i}" for i in range(1, 29)]

        col_groups = [
            columns[0:7],
            columns[7:14],
            columns[14:21],
            columns[21:28]
        ]

        cols = st.columns(4)

        for col_container, group in zip(cols, col_groups):

            with col_container:

                for feature in group:

                    v_values[feature] = st.number_input(
                        feature,
                        value=0.0,
                        format="%.6f"
                    )


        transaction = {
            "Time": time_value,
            **v_values,
            "Amount": amount_value
        }


    # -----------------------------------------------------
    # PREDICTION BUTTON
    # -----------------------------------------------------

    st.write("")

    st.markdown("""
    <div class="input-box">

        <div class="input-title">2️⃣ Run AI Fraud Detection</div>

        <div class="input-description">
            The Agent will coordinate the ML prediction, risk assessment
            and final business decision.
        </div>

    </div>
    """, unsafe_allow_html=True)


    predict_button = st.button(
        "🚀 Run FraudGuard AI",
        type="primary"
    )


    # -----------------------------------------------------
    # OUTPUT
    # -----------------------------------------------------

    if predict_button:

        if transaction is None:

            st.error("Please provide a transaction first.")

        else:

            try:

                with st.spinner(
                    "FraudGuard AI agent is analyzing the transaction..."
                ):

                    result = fraud_detection_agent(transaction)


                fraud_probability = result["fraud_probability"]
                prediction = result["prediction"]
                risk_level = result["risk_level"]
                action = result["recommended_action"]


                st.markdown("""
                <div class="result-box">

                    <div class="result-title">
                        ✅ FraudGuard AI Result
                    </div>

                    <p style="color:#555555;">
                        The transaction has been processed through the
                        complete agentic workflow.
                    </p>

                </div>
                """, unsafe_allow_html=True)


                st.write("")


                # Main result metrics
                r1, r2, r3 = st.columns(3)

                with r1:

                    st.markdown(f"""
                    <div class="metric-card">

                        <div class="metric-label">
                            FRAUD PROBABILITY
                        </div>

                        <div class="metric-number">
                            {fraud_probability * 100:.2f}%
                        </div>

                    </div>
                    """, unsafe_allow_html=True)


                with r2:

                    prediction_text = (
                        "FRAUDULENT"
                        if prediction == 1
                        else "GENUINE"
                    )

                    st.markdown(f"""
                    <div class="metric-card">

                        <div class="metric-label">
                            ML PREDICTION
                        </div>

                        <div class="metric-number">
                            {prediction_text}
                        </div>

                    </div>
                    """, unsafe_allow_html=True)


                with r3:

                    st.markdown(f"""
                    <div class="metric-card">

                        <div class="metric-label">
                            RECOMMENDED ACTION
                        </div>

                        <div class="metric-number">
                            {action}
                        </div>

                    </div>
                    """, unsafe_allow_html=True)


                st.write("")


                # Risk display
                if risk_level == "HIGH":

                    st.markdown(f"""
                    <div class="risk-high">

                        <div class="risk-label">
                            RISK LEVEL
                        </div>

                        <div class="risk-value">
                            🔴 HIGH
                        </div>

                        <p>
                            High probability of fraudulent activity.
                            Recommended action: <b>BLOCK</b>.
                        </p>

                    </div>
                    """, unsafe_allow_html=True)


                elif risk_level == "MEDIUM":

                    st.markdown(f"""
                    <div class="risk-medium">

                        <div class="risk-label">
                            RISK LEVEL
                        </div>

                        <div class="risk-value">
                            🟠 MEDIUM
                        </div>

                        <p>
                            Transaction requires additional verification.
                            Recommended action: <b>REVIEW</b>.
                        </p>

                    </div>
                    """, unsafe_allow_html=True)


                else:

                    st.markdown(f"""
                    <div class="risk-low">

                        <div class="risk-label">
                            RISK LEVEL
                        </div>

                        <div class="risk-value">
                            🟢 LOW
                        </div>

                        <p>
                            Transaction appears to have low fraud risk.
                            Recommended action: <b>APPROVE</b>.
                        </p>

                    </div>
                    """, unsafe_allow_html=True)


                st.write("")

                st.progress(
                    min(max(fraud_probability, 0.0), 1.0),
                    text=f"Fraud Probability: {fraud_probability * 100:.2f}%"
                )


                # Agent execution details
                st.write("")

                st.markdown(
                    '<div class="section-title">🤖 Agent Execution</div>',
                    unsafe_allow_html=True
                )

                a1, a2, a3 = st.columns(3)

                with a1:
                    st.markdown("""
                    <div class="info-card">

                        <h3>🧠 Tool 1 — Prediction</h3>

                        <p>
                            XGBoost analyzes the transaction features
                            and produces the fraud probability.
                        </p>

                        <strong>
                            Output: Fraud Probability
                        </strong>

                    </div>
                    """, unsafe_allow_html=True)


                with a2:
                    st.markdown("""
                    <div class="info-card">

                        <h3>🎯 Tool 2 — Risk Assessment</h3>

                        <p>
                            The agent converts the fraud probability
                            into LOW, MEDIUM or HIGH risk.
                        </p>

                        <strong>
                            Output: Risk Level
                        </strong>

                    </div>
                    """, unsafe_allow_html=True)


                with a3:
                    st.markdown("""
                    <div class="info-card">

                        <h3>🚦 Tool 3 — Decision</h3>

                        <p>
                            The agent maps the risk level to a business
                            action.
                        </p>

                        <strong>
                            Output: APPROVE / REVIEW / BLOCK
                        </strong>

                    </div>
                    """, unsafe_allow_html=True)


            except Exception as e:

                st.error(
                    f"Prediction failed: {e}"
                )

                st.info(
                    "Please verify that final_fraud_model.pkl and "
                    "the required package versions are available."
                )


# =========================================================
# AGENTIC AI
# =========================================================

elif page == "🤖 Agentic AI":

    st.markdown(
        '<div class="section-title">🤖 Agentic AI Decision Engine</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="section-text">

        FraudGuard AI uses a tool-based agentic workflow.
        Instead of only returning a Machine Learning prediction,
        the agent coordinates multiple tools to produce a complete
        fraud-risk decision.

    </div>
    """, unsafe_allow_html=True)

    st.write("")


    # Agent flow
    st.markdown("""
    <div class="info-card">

        <h3>🔄 Agent Workflow</h3>

        <p style="font-size:17px; font-weight:700;">
            Transaction
            →
            ML Prediction
            →
            Risk Assessment
            →
            Business Decision
        </p>

        <p>
            The agent receives a transaction, calls the prediction tool,
            evaluates the resulting fraud probability, determines the
            risk level and finally recommends an action.
        </p>

    </div>
    """, unsafe_allow_html=True)

    st.write("")


    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="info-card">

            <h3>🧠 Tool 1 — Fraud Prediction</h3>

            <p>
                The trained XGBoost model analyzes transaction features
                and returns a fraud probability.
            </p>

            <p>
                <b>Input:</b> Transaction features
            </p>

            <p>
                <b>Output:</b> Fraud probability + prediction
            </p>

        </div>
        """, unsafe_allow_html=True)


    with c2:
        st.markdown("""
        <div class="info-card">

            <h3>🎯 Tool 2 — Risk Assessment</h3>

            <p>
                The agent interprets the fraud probability and assigns
                a risk category.
            </p>

            <p>
                <b>LOW:</b> below 30%
            </p>

            <p>
                <b>MEDIUM:</b> 30% to below 70%
            </p>

            <p>
                <b>HIGH:</b> 70% and above
            </p>

        </div>
        """, unsafe_allow_html=True)


    with c3:
        st.markdown("""
        <div class="info-card">

            <h3>🚦 Tool 3 — Business Decision</h3>

            <p>
                The agent converts the risk level into an operational
                recommendation.
            </p>

            <p>
                <b>LOW → APPROVE</b>
            </p>

            <p>
                <b>MEDIUM → REVIEW</b>
            </p>

            <p>
                <b>HIGH → BLOCK</b>
            </p>

        </div>
        """, unsafe_allow_html=True)


    st.write("")

    st.markdown("""
    <div class="info-card">

        <h3>💡 Why Agentic AI?</h3>

        <p>
            A traditional Machine Learning model only predicts whether
            a transaction is likely to be fraudulent. The agentic layer
            extends this by coordinating prediction, risk assessment
            and decision-making into one automated workflow.
        </p>

        <p>
            This makes the system easier to interpret and demonstrates
            how Machine Learning models can be integrated into
            AI-driven business decision systems.
        </p>

    </div>
    """, unsafe_allow_html=True)


# =========================================================
# ABOUT PROJECT
# =========================================================

elif page == "ℹ️ About Project":

    st.markdown(
        '<div class="section-title">ℹ️ About the Project</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="section-text">
        A Machine Learning and Agentic AI based system for detecting
        fraudulent credit card transactions and generating risk-based
        business decisions.
    </div>
    """, unsafe_allow_html=True)

    st.write("")


    c1, c2 = st.columns(2)

    with c1:

        st.markdown("""
        <div class="info-card">

            <h3>📌 Project Information</h3>

            <p>
                <b>Project:</b>
                Credit Card Fraud Detection
            </p>

            <p>
                <b>Developer:</b>
                Devadharshini Murugan
            </p>

            <p>
                <b>Machine Learning Model:</b>
                XGBoost
            </p>

            <p>
                <b>Application:</b>
                Streamlit
            </p>

            <p>
                <b>AI Layer:</b>
                Tool-Based Agentic AI
            </p>

        </div>
        """, unsafe_allow_html=True)


    with c2:

        st.markdown("""
        <div class="info-card">

            <h3>📊 Dataset</h3>

            <p>
                The project uses a highly imbalanced credit card
                transaction dataset.
            </p>

            <p>
                <b>Total records after duplicate removal:</b>
                25,465
            </p>

            <p>
                <b>Genuine transactions:</b>
                24,992
            </p>

            <p>
                <b>Fraudulent transactions:</b>
                473
            </p>

            <p>
                <b>Fraud percentage:</b>
                1.86%
            </p>

        </div>
        """, unsafe_allow_html=True)


    st.write("")


    st.markdown(
        '<div class="section-title">🏆 Final Model Performance</div>',
        unsafe_allow_html=True
    )


    p1, p2, p3, p4 = st.columns(4)

    with p1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-number">98.73%</div>
            <div class="metric-label">Precision</div>
        </div>
        """, unsafe_allow_html=True)

    with p2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-number">82.11%</div>
            <div class="metric-label">Recall</div>
        </div>
        """, unsafe_allow_html=True)

    with p3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-number">89.66%</div>
            <div class="metric-label">F1 Score</div>
        </div>
        """, unsafe_allow_html=True)

    with p4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-number">98.35%</div>
            <div class="metric-label">ROC-AUC</div>
        </div>
        """, unsafe_allow_html=True)


    st.write("")

    st.markdown("""
    <div class="info-card">

        <h3>🧪 Models Evaluated</h3>

        <p>
            Multiple approaches were evaluated during the project:
        </p>

        <ul>
            <li>Random Forest — Baseline</li>
            <li>Random Forest — Undersampling</li>
            <li>Random Forest — Oversampling</li>
            <li>XGBoost — Baseline</li>
            <li>XGBoost — Undersampling</li>
            <li>XGBoost — Oversampling</li>
        </ul>

        <p>
            The <b>XGBoost Baseline</b> model was selected based on its
            strong overall performance and highest ROC-AUC of
            <b>98.35%</b>.
        </p>

    </div>
    """, unsafe_allow_html=True)


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">
    FraudGuard AI • Credit Card Fraud Detection & Agentic Risk Decision System
    <br>
    Built by <b>Devadharshini Murugan</b>
</div>
""", unsafe_allow_html=True)
