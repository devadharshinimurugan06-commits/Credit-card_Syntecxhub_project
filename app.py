import streamlit as st
import pandas as pd

from agent import fraud_detection_agent


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="FraudGuard AI",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

    /* =========================
       GLOBAL
    ========================= */

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
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3, h4 {
        color: #8f1858 !important;
        font-weight: 800 !important;
    }

    p, label {
        color: #333333 !important;
    }


    /* =========================
       SIDEBAR
    ========================= */

    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #fffafd 0%,
            #ffeef7 100%
        );

        border-right: 1px solid #f1c6da;
    }


    /* =========================
       CREDIT CARD
    ========================= */

    .credit-card {
        background: linear-gradient(
            135deg,
            #8e155c 0%,
            #d71973 50%,
            #8b2bc3 100%
        );

        border-radius: 22px;
        padding: 25px;
        height: 165px;
        margin-bottom: 25px;

        box-shadow:
            0 15px 35px rgba(155, 20, 95, 0.25);

        position: relative;
        overflow: hidden;
    }

    .credit-card:before {
        content: "";
        position: absolute;
        width: 180px;
        height: 180px;
        border-radius: 50%;
        background: rgba(255,255,255,0.08);
        right: -60px;
        top: -70px;
    }

    .credit-card:after {
        content: "";
        position: absolute;
        width: 130px;
        height: 130px;
        border-radius: 50%;
        background: rgba(255,255,255,0.06);
        left: -60px;
        bottom: -70px;
    }

    .card-project {
        color: white !important;
        font-size: 22px;
        font-weight: 900;
        position: relative;
        z-index: 2;
    }

    .card-subtitle {
        color: rgba(255,255,255,0.9) !important;
        font-size: 12px;
        margin-top: 5px;
        position: relative;
        z-index: 2;
    }

    .card-number {
        color: white !important;
        font-size: 18px;
        letter-spacing: 3px;
        margin-top: 25px;
        position: relative;
        z-index: 2;
    }


    /* =========================
       SECTION HEADINGS
    ========================= */

    .section-title {
        color: #9d175b !important;
        font-size: 28px;
        font-weight: 900;
        margin-top: 10px;
        margin-bottom: 8px;
    }

    .section-text {
        color: #4b4b4b !important;
        font-size: 16px;
        line-height: 1.6;
        margin-bottom: 22px;
    }


    /* =========================
       WHITE CARDS
    ========================= */

    .info-card {
        background: white;
        border: 1px solid #efc6da;
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 18px;

        box-shadow:
            0 8px 25px rgba(120,30,90,0.07);
    }

    .info-card h3 {
        color: #9d175b !important;
        margin-top: 0;
    }

    .info-card p {
        color: #444444 !important;
        line-height: 1.6;
    }


    /* =========================
       WORKFLOW CARDS
    ========================= */

    .workflow-card {
        background: white;
        border: 1px solid #efc6da;
        border-radius: 18px;
        padding: 22px;
        text-align: center;
        min-height: 145px;

        box-shadow:
            0 8px 22px rgba(120,30,90,0.07);
    }

    .workflow-icon {
        font-size: 30px;
        margin-bottom: 8px;
    }

    .workflow-title {
        color: #8f1858 !important;
        font-size: 17px;
        font-weight: 800;
    }

    .workflow-text {
        color: #555555 !important;
        font-size: 13px;
        margin-top: 8px;
        line-height: 1.5;
    }


    /* =========================
       METRIC CARDS
    ========================= */

    .metric-card {
        background: white;
        border: 1px solid #efc6da;
        border-radius: 18px;
        padding: 20px;
        text-align: center;

        box-shadow:
            0 8px 20px rgba(120,30,90,0.07);
    }

    .metric-value {
        color: #b31368 !important;
        font-size: 28px;
        font-weight: 900;
    }

    .metric-label {
        color: #555555 !important;
        font-size: 13px;
        margin-top: 5px;
    }


    /* =========================
       RESULT
    ========================= */

    .result-card {
        background: white;
        border: 2px solid #d71973;
        border-radius: 22px;
        padding: 25px;
        margin-top: 20px;

        box-shadow:
            0 12px 30px rgba(120,30,90,0.10);
    }

    .result-title {
        color: #8f1858 !important;
        font-size: 25px;
        font-weight: 900;
        margin-bottom: 15px;
    }


    /* =========================
       RISK
    ========================= */

    .risk-low {
        background: #effaf2;
        border: 2px solid #3aaa65;
        border-radius: 18px;
        padding: 22px;
        text-align: center;
        margin-top: 18px;
    }

    .risk-medium {
        background: #fff8e8;
        border: 2px solid #e3a52a;
        border-radius: 18px;
        padding: 22px;
        text-align: center;
        margin-top: 18px;
    }

    .risk-high {
        background: #fff0f0;
        border: 2px solid #e04b4b;
        border-radius: 18px;
        padding: 22px;
        text-align: center;
        margin-top: 18px;
    }

    .risk-title {
        font-size: 14px;
        color: #555555 !important;
    }

    .risk-value {
        font-size: 30px;
        font-weight: 900;
        color: #222222 !important;
    }


    /* =========================
       BUTTON
    ========================= */

    .stButton > button {
        width: 100%;
        border-radius: 12px;
        border: none;

        background: linear-gradient(
            90deg,
            #c81769,
            #8d28bd
        );

        color: white !important;
        font-weight: 800;
        font-size: 16px;

        padding: 12px 20px;

        box-shadow:
            0 8px 18px rgba(150,30,110,0.20);
    }

    .stButton > button:hover {
        transform: translateY(-1px);
    }


    /* =========================
       FOOTER
    ========================= */

    .footer {
        text-align: center;
        padding: 35px 0 10px 0;
        color: #666666 !important;
        font-size: 13px;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# CONSTANTS
# ============================================================

FEATURE_COLUMNS = (
    ["Time"]
    + [f"V{i}" for i in range(1, 29)]
    + ["Amount"]
)

DATASET_FILE = "creditcard_small.csv"


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("""
    <div class="credit-card">

        <div class="card-project">
            💳 FraudGuard AI
        </div>

        <div class="card-subtitle">
            Credit Card Fraud Detection
        </div>

        <div class="card-number">
            ••••  ••••  ••••  2026
        </div>

    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        "### Navigation"
    )

    st.caption("FraudGuard AI Control Panel")

    page = st.radio(
        "Select Page",
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

        <div style="
            color:#9d175b;
            font-weight:800;
        ">
            Project Owner
        </div>

        <div style="
            color:#333333;
            margin-top:5px;
        ">
            Devadharshini Murugan
        </div>

    </div>
    """, unsafe_allow_html=True)


# ============================================================
# DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    st.markdown(
        '<div class="section-title">💳 FraudGuard AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-text">
            Credit Card Fraud Detection using Machine Learning
            and Agentic AI based risk decision support.
        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # PROJECT NAME CARD
    # --------------------------------------------------------

    st.markdown("""
    <div class="info-card">

        <h3>Credit Card Fraud Detection</h3>

        <p>
            FraudGuard AI analyzes credit card transactions using
            a trained XGBoost model and converts the prediction
            into a practical risk-based business decision.
        </p>

    </div>
    """, unsafe_allow_html=True)


    # --------------------------------------------------------
    # HOW SYSTEM WORKS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">⚙️ How the System Works</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown("""
        <div class="workflow-card">
            <div class="workflow-icon">💳</div>
            <div class="workflow-title">1. Transaction</div>
            <div class="workflow-text">
                Transaction details are provided as input.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="workflow-card">
            <div class="workflow-icon">🧠</div>
            <div class="workflow-title">2. XGBoost</div>
            <div class="workflow-text">
                The trained model predicts fraud probability.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="workflow-card">
            <div class="workflow-icon">🎯</div>
            <div class="workflow-title">3. Risk Assessment</div>
            <div class="workflow-text">
                Agentic AI converts probability into risk.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown("""
        <div class="workflow-card">
            <div class="workflow-icon">🚦</div>
            <div class="workflow-title">4. Decision</div>
            <div class="workflow-text">
                The system recommends Approve, Review or Block.
            </div>
        </div>
        """, unsafe_allow_html=True)


    # --------------------------------------------------------
    # MODEL PERFORMANCE
    # --------------------------------------------------------

    st.markdown("")
    st.markdown(
        '<div class="section-title">📊 Model Performance</div>',
        unsafe_allow_html=True
    )

    m1, m2, m3, m4 = st.columns(4)

    metrics = [
        ("98.73%", "Precision"),
        ("82.11%", "Recall"),
        ("89.66%", "F1 Score"),
        ("98.35%", "ROC-AUC")
    ]

    for col, (value, label) in zip(
        [m1, m2, m3, m4],
        metrics
    ):
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-value">
                        {value}
                    </div>
                    <div class="metric-label">
                        {label}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


    # --------------------------------------------------------
    # OBJECTIVE
    # --------------------------------------------------------

    st.markdown("")

    st.markdown("""
    <div class="info-card">

        <h3>🎯 Project Objective</h3>

        <p>
            The objective is to identify potentially fraudulent
            credit card transactions and provide a risk-based
            recommendation for each transaction.
        </p>

        <p>
            Since fraud transactions are highly imbalanced,
            Precision, Recall, F1 Score and ROC-AUC are considered
            important evaluation measures.
        </p>

    </div>
    """, unsafe_allow_html=True)


# ============================================================
# FRAUD DETECTION
# ============================================================

elif page == "🔍 Fraud Detection":

    st.markdown(
        '<div class="section-title">🔍 Fraud Detection</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-text">
            Provide a credit card transaction and run FraudGuard AI.
            The system will return the fraud probability, prediction,
            risk level and recommended action.
        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # INPUT METHOD
    # --------------------------------------------------------

    st.markdown("### 1️⃣ Provide Transaction")

    input_method = st.radio(
        "Choose input method",
        [
            "Use Project CSV",
            "Upload CSV",
            "Enter Manually"
        ],
        horizontal=True
    )


    transaction = None
    selected_row = None


    # ========================================================
    # PROJECT CSV
    # ========================================================

    if input_method == "Use Project CSV":

        try:

            df = pd.read_csv(DATASET_FILE)

            if not all(
                feature in df.columns
                for feature in FEATURE_COLUMNS
            ):
                st.error(
                    "The project CSV does not contain the required "
                    "transaction columns."
                )

            else:

                row_number = st.number_input(
                    "Select transaction row",
                    min_value=0,
                    max_value=len(df) - 1,
                    value=0,
                    step=1
                )

                selected_row = df.iloc[int(row_number)]

                transaction = {
                    feature: float(selected_row[feature])
                    for feature in FEATURE_COLUMNS
                }

                st.success(
                    f"Transaction row {int(row_number)} loaded successfully."
                )

                with st.expander("View Selected Transaction"):

                    display_df = pd.DataFrame(
                        [transaction]
                    )

                    st.dataframe(
                        display_df,
                        use_container_width=True
                    )


        except FileNotFoundError:

            st.error(
                f"{DATASET_FILE} was not found. "
                "Make sure it is in the same GitHub folder as app.py."
            )

        except Exception as e:

            st.error(
                f"Could not load the project CSV: {e}"
            )


    # ========================================================
    # UPLOAD CSV
    # ========================================================

    elif input_method == "Upload CSV":

        uploaded_file = st.file_uploader(
            "Upload your credit card transaction CSV",
            type=["csv"]
        )

        if uploaded_file is not None:

            try:

                upload_df = pd.read_csv(uploaded_file)

                st.success(
                    f"CSV loaded successfully — {len(upload_df):,} rows."
                )

                missing_columns = [
                    feature
                    for feature in FEATURE_COLUMNS
                    if feature not in upload_df.columns
                ]

                if missing_columns:

                    st.error(
                        "Missing required columns: "
                        + ", ".join(missing_columns)
                    )

                else:

                    row_number = st.number_input(
                        "Select transaction row",
                        min_value=0,
                        max_value=len(upload_df) - 1,
                        value=0,
                        step=1
                    )

                    selected_row = upload_df.iloc[
                        int(row_number)
                    ]

                    transaction = {
                        feature: float(selected_row[feature])
                        for feature in FEATURE_COLUMNS
                    }

                    with st.expander(
                        "View Selected Transaction"
                    ):

                        st.dataframe(
                            pd.DataFrame([transaction]),
                            use_container_width=True
                        )

            except Exception as e:

                st.error(
                    f"Could not read the uploaded CSV: {e}"
                )


    # ========================================================
    # MANUAL INPUT
    # ========================================================

    else:

        st.info(
            "Enter the transaction features below. "
            "The model expects Time, V1–V28 and Amount."
        )

        time_value = st.number_input(
            "Time",
            value=0.0
        )

        amount_value = st.number_input(
            "Amount",
            min_value=0.0,
            value=100.0
        )

        st.markdown("#### PCA Transaction Features")

        v_values = {}

        groups = [
            [f"V{i}" for i in range(1, 8)],
            [f"V{i}" for i in range(8, 15)],
            [f"V{i}" for i in range(15, 22)],
            [f"V{i}" for i in range(22, 29)]
        ]

        input_cols = st.columns(4)

        for container, group in zip(
            input_cols,
            groups
        ):

            with container:

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


    # --------------------------------------------------------
    # PREDICT
    # --------------------------------------------------------

    st.markdown("### 2️⃣ Run Fraud Detection")

    detect_button = st.button(
        "🚀 Detect Fraud",
        type="primary"
    )


    # ========================================================
    # OUTPUT
    # ========================================================

    if detect_button:

        if transaction is None:

            st.warning(
                "Please provide a transaction first."
            )

        else:

            try:

                with st.spinner(
                    "FraudGuard AI is analyzing the transaction..."
                ):

                    result = fraud_detection_agent(
                        transaction
                    )


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


                # ------------------------------------------------
                # RESULT
                # ------------------------------------------------

                st.markdown(
                    '<div class="section-title">✅ Fraud Detection Result</div>',
                    unsafe_allow_html=True
                )


                r1, r2, r3 = st.columns(3)


                with r1:

                    st.markdown(
                        f"""
                        <div class="metric-card">

                            <div class="metric-value">
                                {fraud_probability * 100:.2f}%
                            </div>

                            <div class="metric-label">
                                FRAUD PROBABILITY
                            </div>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )


                with r2:

                    st.markdown(
                        f"""
                        <div class="metric-card">

                            <div class="metric-value">
                                {prediction_text}
                            </div>

                            <div class="metric-label">
                                ML PREDICTION
                            </div>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )


                with r3:

                    st.markdown(
                        f"""
                        <div class="metric-card">

                            <div class="metric-value">
                                {action}
                            </div>

                            <div class="metric-label">
                                RECOMMENDED ACTION
                            </div>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )


                # ------------------------------------------------
                # RISK LEVEL
                # ------------------------------------------------

                if risk_level == "HIGH":

                    st.markdown(
                        """
                        <div class="risk-high">

                            <div class="risk-title">
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
                        """,
                        unsafe_allow_html=True
                    )

                elif risk_level == "MEDIUM":

                    st.markdown(
                        """
                        <div class="risk-medium">

                            <div class="risk-title">
                                RISK LEVEL
                            </div>

                            <div class="risk-value">
                                🟠 MEDIUM
                            </div>

                            <p>
                                The transaction requires additional
                                verification.
                                Recommended action: <b>REVIEW</b>.
                            </p>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                else:

                    st.markdown(
                        """
                        <div class="risk-low">

                            <div class="risk-title">
                                RISK LEVEL
                            </div>

                            <div class="risk-value">
                                🟢 LOW
                            </div>

                            <p>
                                The transaction appears to have low
                                fraud risk.
                                Recommended action: <b>APPROVE</b>.
                            </p>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )


                # ------------------------------------------------
                # PROBABILITY BAR
                # ------------------------------------------------

                st.markdown("")

                st.progress(
                    min(
                        max(fraud_probability, 0.0),
                        1.0
                    ),
                    text=(
                        f"Fraud Probability: "
                        f"{fraud_probability * 100:.2f}%"
                    )
                )


                # ------------------------------------------------
                # SIMPLE AGENT EXPLANATION
                # ------------------------------------------------

                st.markdown(
                    '<div class="section-title">🤖 Agentic AI Decision</div>',
                    unsafe_allow_html=True
                )


                a1, a2, a3 = st.columns(3)


                with a1:

                    st.markdown("""
                    <div class="workflow-card">

                        <div class="workflow-icon">
                            🧠
                        </div>

                        <div class="workflow-title">
                            XGBoost Prediction
                        </div>

                        <div class="workflow-text">
                            The trained XGBoost model evaluates
                            the transaction and generates the
                            fraud probability.
                        </div>

                    </div>
                    """, unsafe_allow_html=True)


                with a2:

                    st.markdown("""
                    <div class="workflow-card">

                        <div class="workflow-icon">
                            🎯
                        </div>

                        <div class="workflow-title">
                            Risk Assessment
                        </div>

                        <div class="workflow-text">
                            Agentic AI interprets the fraud
                            probability and assigns a risk level.
                        </div>

                    </div>
                    """, unsafe_allow_html=True)


                with a3:

                    st.markdown("""
                    <div class="workflow-card">

                        <div class="workflow-icon">
                            🚦
                        </div>

                        <div class="workflow-title">
                            Business Decision
                        </div>

                        <div class="workflow-text">
                            The agent recommends Approve,
                            Review or Block.
                        </div>

                    </div>
                    """, unsafe_allow_html=True)


            except Exception as e:

                st.error(
                    f"Prediction failed: {e}"
                )

                st.info(
                    "Check that agent.py, final_fraud_model.pkl "
                    "and the required dependencies are available."
                )


# ============================================================
# AGENTIC AI
# ============================================================

elif page == "🤖 Agentic AI":

    st.markdown(
        '<div class="section-title">🤖 Agentic AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-text">
            The Agentic AI layer extends the Machine Learning
            prediction into a complete risk-based decision workflow.
        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # FLOW
    # --------------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    agent_steps = [
        (
            "💳",
            "Transaction",
            "Transaction features are provided as input."
        ),
        (
            "🧠",
            "ML Prediction",
            "XGBoost generates the fraud probability."
        ),
        (
            "🎯",
            "Risk Assessment",
            "The agent assigns Low, Medium or High risk."
        ),
        (
            "🚦",
            "Decision",
            "The system recommends Approve, Review or Block."
        )
    ]

    for col, (icon, title, text) in zip(
        [c1, c2, c3, c4],
        agent_steps
    ):

        with col:

            st.markdown(
                f"""
                <div class="workflow-card">

                    <div class="workflow-icon">
                        {icon}
                    </div>

                    <div class="workflow-title">
                        {title}
                    </div>

                    <div class="workflow-text">
                        {text}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


    st.markdown("")

    # --------------------------------------------------------
    # EXPLANATION
    # --------------------------------------------------------

    st.markdown("""
    <div class="info-card">

        <h3>How Agentic AI Works</h3>

        <p>
            The Agentic AI workflow receives a transaction and
            coordinates the fraud prediction, risk assessment
            and business decision steps.
        </p>

        <p>
            The XGBoost model provides the Machine Learning
            prediction. The agent then interprets that probability
            and converts it into a practical business action.
        </p>

    </div>
    """, unsafe_allow_html=True)


    # --------------------------------------------------------
    # RISK RULES
    # --------------------------------------------------------

    st.markdown("### Risk-Based Decision")

    r1, r2, r3 = st.columns(3)

    with r1:

        st.markdown("""
        <div class="risk-low">

            <div class="risk-value">
                🟢 LOW
            </div>

            <p>
                Fraud probability below 30%
            </p>

            <strong>
                APPROVE
            </strong>

        </div>
        """, unsafe_allow_html=True)


    with r2:

        st.markdown("""
        <div class="risk-medium">

            <div class="risk-value">
                🟠 MEDIUM
            </div>

            <p>
                Fraud probability from 30% to below 70%
            </p>

            <strong>
                REVIEW
            </strong>

        </div>
        """, unsafe_allow_html=True)


    with r3:

        st.markdown("""
        <div class="risk-high">

            <div class="risk-value">
                🔴 HIGH
            </div>

            <p>
                Fraud probability 70% and above
            </p>

            <strong>
                BLOCK
            </strong>

        </div>
        """, unsafe_allow_html=True)


# ============================================================
# ABOUT PROJECT
# ============================================================

elif page == "ℹ️ About Project":

    st.markdown(
        '<div class="section-title">ℹ️ About the Project</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-text">
            A Machine Learning and Agentic AI based system for
            detecting fraudulent credit card transactions and
            generating risk-based business decisions.
        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # PROJECT DETAILS
    # --------------------------------------------------------

    st.markdown("""
    <div class="info-card">

        <h3>📌 Project Information</h3>

        <p>
            <b>Project:</b>
            Credit Card Fraud Detection
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
            Agentic AI
        </p>

    </div>
    """, unsafe_allow_html=True)


    # --------------------------------------------------------
    # DATASET
    # --------------------------------------------------------

    st.markdown("""
    <div class="info-card">

        <h3>📊 Dataset Information</h3>

        <p>
            The project uses a highly imbalanced credit card
            transaction dataset.
        </p>

        <p>
            <b>Total records:</b> 25,465
        </p>

        <p>
            <b>Genuine transactions:</b> 24,992
        </p>

        <p>
            <b>Fraudulent transactions:</b> 473
        </p>

        <p>
            <b>Fraud percentage:</b> 1.86%
        </p>

    </div>
    """, unsafe_allow_html=True)


    # --------------------------------------------------------
    # MODEL DEVELOPMENT
    # --------------------------------------------------------

    st.markdown("""
    <div class="info-card">

        <h3>🧪 Model Development</h3>

        <p>
            Multiple approaches were evaluated to handle the
            class imbalance problem.
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
            XGBoost was selected as the final model based on
            its overall performance.
        </p>

    </div>
    """, unsafe_allow_html=True)


    # --------------------------------------------------------
    # PERFORMANCE
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">🏆 Final Model Performance</div>',
        unsafe_allow_html=True
    )

    p1, p2, p3, p4 = st.columns(4)

    performance = [
        ("98.73%", "Precision"),
        ("82.11%", "Recall"),
        ("89.66%", "F1 Score"),
        ("98.35%", "ROC-AUC")
    ]

    for col, (value, label) in zip(
        [p1, p2, p3, p4],
        performance
    ):

        with col:

            st.markdown(
                f"""
                <div class="metric-card">

                    <div class="metric-value">
                        {value}
                    </div>

                    <div class="metric-label">
                        {label}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


    # --------------------------------------------------------
    # TECHNOLOGIES
    # --------------------------------------------------------

    st.markdown("")

    st.markdown("""
    <div class="info-card">

        <h3>🛠️ Technologies Used</h3>

        <p>
            Python · Pandas · Scikit-learn · XGBoost ·
            Streamlit · Agentic AI
        </p>

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
