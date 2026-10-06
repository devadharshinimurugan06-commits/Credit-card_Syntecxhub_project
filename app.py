import streamlit as st
import pandas as pd

from agent import fraud_detection_agent


# =========================================================
# PAGE CONFIGURATION
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

    /* ---------- Main Background ---------- */

    .stApp {
        background: linear-gradient(
            135deg,
            #fff5f9 0%,
            #ffeaf3 50%,
            #fff8fb 100%
        );
    }

    /* ---------- Main Container ---------- */

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1250px;
    }

    /* ---------- Sidebar ---------- */

    [data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #ffffff 0%,
            #fff0f6 100%
        );
        border-right: 1px solid #f3c6da;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #8e2454;
    }

    /* ---------- Hero Header ---------- */

    .hero {
        background: linear-gradient(
            135deg,
            #c2185b,
            #e91e63,
            #9c27b0
        );
        padding: 35px;
        border-radius: 25px;
        color: white;
        box-shadow: 0 12px 35px rgba(194, 24, 91, 0.25);
        margin-bottom: 25px;
    }

    .hero-title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .hero-subtitle {
        font-size: 17px;
        opacity: 0.95;
    }

    /* ---------- Credit Card Logo ---------- */

    .credit-card-logo {
        width: 95px;
        height: 62px;
        background: linear-gradient(
            135deg,
            #ffffff,
            #ffe1ee
        );
        border-radius: 12px;
        padding: 10px;
        position: relative;
        box-shadow: 0 8px 20px rgba(0,0,0,0.18);
        margin-bottom: 15px;
    }

    .card-chip {
        width: 25px;
        height: 18px;
        background: #f7c948;
        border-radius: 5px;
        margin-top: 7px;
    }

    .card-line {
        width: 65px;
        height: 5px;
        background: #c2185b;
        border-radius: 10px;
        margin-top: 8px;
    }

    /* ---------- White Cards ---------- */

    .white-card {
        background: white;
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 7px 25px rgba(156, 39, 112, 0.10);
        border: 1px solid #f6d4e2;
        margin-bottom: 20px;
    }

    /* ---------- Section Titles ---------- */

    .section-title {
        color: #8e2454;
        font-size: 25px;
        font-weight: 750;
        margin-bottom: 12px;
    }

    /* ---------- Agent Flow ---------- */

    .agent-box {
        background: linear-gradient(
            135deg,
            #ffffff,
            #fff1f7
        );
        border: 2px solid #f4c2d8;
        border-radius: 20px;
        padding: 22px;
        text-align: center;
        min-height: 135px;
        box-shadow: 0 5px 18px rgba(194,24,91,0.08);
    }

    .agent-icon {
        font-size: 32px;
    }

    .agent-title {
        color: #8e2454;
        font-size: 17px;
        font-weight: 700;
    }

    .agent-text {
        color: #666;
        font-size: 13px;
    }

    /* ---------- Metric Cards ---------- */

    .metric-card {
        background: white;
        border-radius: 18px;
        padding: 20px;
        text-align: center;
        border: 1px solid #f2ccdc;
        box-shadow: 0 6px 20px rgba(194,24,91,0.08);
    }

    .metric-label {
        color: #777;
        font-size: 14px;
    }

    .metric-value {
        color: #c2185b;
        font-size: 28px;
        font-weight: 800;
    }

    /* ---------- Risk Cards ---------- */

    .high-risk {
        background: #fff0f0;
        border: 2px solid #ff5c5c;
        color: #b71c1c;
        padding: 22px;
        border-radius: 18px;
        text-align: center;
        font-size: 20px;
        font-weight: 700;
    }

    .medium-risk {
        background: #fff8e1;
        border: 2px solid #ffc107;
        color: #8a6100;
        padding: 22px;
        border-radius: 18px;
        text-align: center;
        font-size: 20px;
        font-weight: 700;
    }

    .low-risk {
        background: #edfff5;
        border: 2px solid #36c77b;
        color: #08783f;
        padding: 22px;
        border-radius: 18px;
        text-align: center;
        font-size: 20px;
        font-weight: 700;
    }

    /* ---------- Buttons ---------- */

    .stButton > button {
        background: linear-gradient(
            135deg,
            #c2185b,
            #e91e63
        );
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 25px;
        font-weight: 700;
        font-size: 16px;
        box-shadow: 0 5px 15px rgba(194,24,91,0.20);
    }

    .stButton > button:hover {
        background: linear-gradient(
            135deg,
            #9c1749,
            #c2185b
        );
        color: white;
    }

    /* ---------- Footer ---------- */

    .footer {
        text-align: center;
        color: #9a6b80;
        padding: 25px;
        font-size: 13px;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("""
    <div style="text-align:center;">

        <div class="credit-card-logo" style="margin:auto;">
            <div class="card-chip"></div>
            <div class="card-line"></div>
        </div>

        <h2>FraudGuard AI</h2>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### 🧭 Navigation")

    page = st.radio(
        "Go to",
        [
            "🏠 Dashboard",
            "🔍 Fraud Detection",
            "🤖 Agentic AI",
            "ℹ️ About Project"
        ]
    )

    st.markdown("---")

    st.markdown("### 🛡️ Risk Levels")

    st.markdown("🟢 **LOW** — Approve")
    st.markdown("🟡 **MEDIUM** — Review")
    st.markdown("🔴 **HIGH** — Block")

    st.markdown("---")

    st.caption("Machine Learning + Agentic Decision System")


# =========================================================
# HERO HEADER
# =========================================================

st.markdown("""
<div class="hero">

    <div class="credit-card-logo">
        <div class="card-chip"></div>
        <div class="card-line"></div>
    </div>

    <div class="hero-title">
        FraudGuard AI
    </div>

    <div class="hero-subtitle">
        Intelligent Credit Card Fraud Detection & Agentic Risk Decision System
    </div>

</div>
""", unsafe_allow_html=True)


# =========================================================
# DASHBOARD PAGE
# =========================================================

if page == "🏠 Dashboard":

    st.markdown(
        '<div class="section-title">✨ Intelligent Fraud Protection</div>',
        unsafe_allow_html=True
    )

    st.write(
        "FraudGuard AI combines a trained Machine Learning model "
        "with an Agentic AI decision workflow to analyze transactions "
        "and recommend the appropriate business action."
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Agent workflow

    st.markdown(
        '<div class="section-title">🤖 How the Agentic AI Works</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="agent-box">
            <div class="agent-icon">💳</div>
            <div class="agent-title">Transaction</div>
            <div class="agent-text">
                Transaction data enters the system
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="agent-box">
            <div class="agent-icon">🧠</div>
            <div class="agent-title">ML Prediction</div>
            <div class="agent-text">
                XGBoost predicts fraud probability
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="agent-box">
            <div class="agent-icon">🎯</div>
            <div class="agent-title">Risk Assessment</div>
            <div class="agent-text">
                Agent determines transaction risk
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="agent-box">
            <div class="agent-icon">🚦</div>
            <div class="agent-title">Decision</div>
            <div class="agent-text">
                Approve, Review or Block
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Project highlights

    st.markdown(
        '<div class="section-title">📊 Project Highlights</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    metrics = [
        ("🎯", "Model", "XGBoost"),
        ("📈", "ROC-AUC", "0.9835"),
        ("🔎", "Fraud Recall", "82.11%"),
        ("🛡️", "Precision", "98.73%")
    ]

    for col, (icon, label, value) in zip(
        [col1, col2, col3, col4],
        metrics
    ):
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div style="font-size:28px;">{icon}</div>
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True
            )


# =========================================================
# FRAUD DETECTION PAGE
# =========================================================

elif page == "🔍 Fraud Detection":

    st.markdown(
        '<div class="section-title">🔍 Transaction Fraud Analysis</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Upload a transaction CSV or use a transaction from the "
        "project dataset for demonstration."
    )

    input_method = st.radio(
        "Choose input method:",
        ["📁 Upload Transaction CSV", "🧪 Demo Transaction"],
        horizontal=True
    )

    feature_columns = [
        "Time",
        "V1", "V2", "V3", "V4", "V5", "V6", "V7",
        "V8", "V9", "V10", "V11", "V12", "V13", "V14",
        "V15", "V16", "V17", "V18", "V19", "V20", "V21",
        "V22", "V23", "V24", "V25", "V26", "V27", "V28",
        "Amount"
    ]

    transaction = None

    # -----------------------------------------------------
    # CSV Upload
    # -----------------------------------------------------

    if input_method == "📁 Upload Transaction CSV":

        uploaded_file = st.file_uploader(
            "Upload a transaction CSV",
            type=["csv"]
        )

        if uploaded_file is not None:

            transaction_df = pd.read_csv(uploaded_file)

            missing_columns = [
                col for col in feature_columns
                if col not in transaction_df.columns
            ]

            if missing_columns:

                st.error(
                    "Missing columns: "
                    + ", ".join(missing_columns)
                )

            elif len(transaction_df) == 0:

                st.error("The uploaded CSV is empty.")

            else:

                transaction = transaction_df[
                    feature_columns
                ].iloc[0].to_dict()

                st.success(
                    "Transaction loaded successfully!"
                )

                st.dataframe(
                    transaction_df[feature_columns].head(1),
                    use_container_width=True
                )

    # -----------------------------------------------------
    # Demo Transaction
    # -----------------------------------------------------

    else:

        try:

            dataset = pd.read_csv(
                "creditcard_small.csv"
            )

            transaction_index = st.number_input(
                "Select transaction number",
                min_value=0,
                max_value=len(dataset) - 1,
                value=0,
                step=1
            )

            selected = dataset.iloc[
                int(transaction_index)
            ]

            transaction = selected[
                feature_columns
            ].to_dict()

            st.info(
                "A transaction from the project dataset "
                "will be analyzed."
            )

            st.dataframe(
                pd.DataFrame([transaction]),
                use_container_width=True
            )

        except FileNotFoundError:

            st.error(
                "creditcard_small.csv was not found."
            )

    # -----------------------------------------------------
    # Analyze Button
    # -----------------------------------------------------

    if transaction is not None:

        if st.button(
            "🚀 Analyze Transaction with Agentic AI",
            type="primary"
        ):

            with st.spinner(
                "🤖 Agent is analyzing the transaction..."
            ):

                result = fraud_detection_agent(
                    transaction
                )

            fraud_probability = result[
                "fraud_probability"
            ]

            risk_level = result[
                "risk_level"
            ]

            action = result[
                "recommended_action"
            ]

            st.divider()

            st.markdown(
                '<div class="section-title">'
                '🤖 Agentic AI Decision'
                '</div>',
                unsafe_allow_html=True
            )

            # Metrics

            col1, col2, col3 = st.columns(3)

            with col1:

                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">
                            Fraud Probability
                        </div>
                        <div class="metric-value">
                            {fraud_probability * 100:.2f}%
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col2:

                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">
                            Risk Level
                        </div>
                        <div class="metric-value">
                            {risk_level}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col3:

                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">
                            Recommended Action
                        </div>
                        <div class="metric-value">
                            {action}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.markdown("<br>", unsafe_allow_html=True)

            # Probability bar

            st.write("### 📊 Fraud Probability")

            st.progress(
                fraud_probability
            )

            # Risk decision

            if risk_level == "HIGH":

                st.markdown(
                    """
                    <div class="high-risk">
                        🚨 HIGH RISK<br>
                        Transaction should be BLOCKED
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            elif risk_level == "MEDIUM":

                st.markdown(
                    """
                    <div class="medium-risk">
                        ⚠️ MEDIUM RISK<br>
                        Transaction requires REVIEW
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    """
                    <div class="low-risk">
                        ✅ LOW RISK<br>
                        Transaction can be APPROVED
                    </div>
                    """,
                    unsafe_allow_html=True
                )


# =========================================================
# AGENTIC AI PAGE
# =========================================================

elif page == "🤖 Agentic AI":

    st.markdown(
        '<div class="section-title">'
        '🤖 Agentic AI Decision Engine'
        '</div>',
        unsafe_allow_html=True
    )

    st.write(
        "FraudGuard AI uses a tool-based agentic workflow. "
        "The agent coordinates the Machine Learning prediction, "
        "risk assessment and business decision tools."
    )

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown("""
        <div class="white-card">

        ### 🧠 Tool 1 — Prediction

        The XGBoost model analyzes the transaction and
        produces a fraud probability.

        **Output:** Fraud Probability

        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown("""
        <div class="white-card">

        ### 🎯 Tool 2 — Risk

        The agent converts the probability into
        LOW, MEDIUM or HIGH risk.

        **Output:** Risk Level

        </div>
        """, unsafe_allow_html=True)

    with col3:

        st.markdown("""
        <div class="white-card">

        ### 🚦 Tool 3 — Decision

        The agent recommends an appropriate
        business action.

        **Output:** APPROVE / REVIEW / BLOCK

        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.info(
        "💡 This agentic workflow demonstrates how an AI system "
        "can combine prediction tools with automated business "
        "decision-making."
    )


# =========================================================
# ABOUT PAGE
# =========================================================

elif page == "ℹ️ About Project":

    st.markdown(
        '<div class="section-title">'
        'ℹ️ About FraudGuard AI'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="white-card">

    ### 💳 Credit Card Fraud Detection

    This project focuses on detecting fraudulent credit card
    transactions in a highly imbalanced dataset.

    ### 🔬 Machine Learning

    Multiple approaches were evaluated including:

    - Random Forest
    - Random Forest with undersampling
    - Random Forest with oversampling
    - XGBoost
    - XGBoost with undersampling
    - XGBoost with oversampling

    ### 🏆 Selected Model

    **XGBoost Baseline**

    - Precision: **98.73%**
    - Recall: **82.11%**
    - F1 Score: **89.66%**
    - ROC-AUC: **98.35%**

    ### 🤖 Agentic AI

    The final system adds an agentic decision layer that
    converts ML predictions into practical business actions:

    **Fraud Prediction → Risk Assessment → Business Decision**

    </div>
    """, unsafe_allow_html=True)


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">
    🛡️ <b>FraudGuard AI</b> |
    Intelligent Credit Card Fraud Detection |
    Machine Learning + Agentic AI
</div>
""", unsafe_allow_html=True)
