import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from src.fraud_predictor import predict_transactions
from src.llm_explainer import explain_transaction
from src.rag_engine import answer_policy_question
from src.report_generator import generate_report
from src.train_model import train_model

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "sample_transactions.csv"
METRICS_PATH = ROOT / "models" / "metrics.json"

st.set_page_config(
    page_title="FinTech GenAI Fraud Risk Assistant",
    layout="wide"
)

st.title("AI-Powered FinTech Fraud Risk & Compliance Assistant")
st.caption("Machine Learning + GenAI-style Explanation + RAG-style Compliance Q&A + Dashboard + PDF Report")

with st.sidebar:
    st.header("Navigation")
    page = st.radio(
        "Go to",
        [
            "Home",
            "Upload & Predict",
            "Fraud Analytics Dashboard",
            "Compliance Q&A",
            "Generate Report",
            "Model Metrics"
        ]
    )

    if st.button("Train / Retrain Model"):
        with st.spinner("Training model..."):
            metrics = train_model()
        st.success("Model trained successfully.")
        st.json(metrics)

if page == "Home":
    st.subheader("Project Objective")
    st.write("""
    This advanced FinTech project detects suspicious transactions, explains fraud risk in simple language,
    answers compliance questions from policy documents, and generates fraud investigation reports.
    """)
    st.markdown("""
    **Core Features**
    - Fraud detection using Machine Learning
    - Risk score and fraud probability
    - GenAI-style explanation for suspicious transactions
    - RAG-style policy/compliance question answering
    - Interactive fraud analytics dashboard
    - PDF fraud investigation report
    """)
    st.info("Use the sidebar to start. The app includes sample transaction data, so you can run it immediately.")

elif page == "Upload & Predict":
    st.subheader("Upload Transaction CSV or Use Sample Data")

    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_csv(DATA_PATH)

    st.write("Data Preview")
    st.dataframe(df.head(20), use_container_width=True)

    if st.button("Run Fraud Prediction"):
        result_df = predict_transactions(df)
        st.session_state["result_df"] = result_df

        st.success("Prediction completed.")
        st.dataframe(result_df, use_container_width=True)

        csv = result_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download Prediction CSV",
            data=csv,
            file_name="fraud_predictions.csv",
            mime="text/csv"
        )

        st.subheader("AI Explanation for First High-Risk Transaction")
        high_risk = result_df[result_df["risk_level"] == "High Risk"]
        sample_row = high_risk.iloc[0] if len(high_risk) else result_df.iloc[0]
        explanation = explain_transaction(sample_row)
        st.write(explanation)

elif page == "Fraud Analytics Dashboard":
    st.subheader("Fraud Analytics Dashboard")

    if "result_df" in st.session_state:
        result_df = st.session_state["result_df"]
    else:
        result_df = predict_transactions(pd.read_csv(DATA_PATH))

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Transactions", len(result_df))
    col2.metric("Predicted Fraud", int(result_df["prediction"].sum()))
    col3.metric("Avg Risk Score", round(result_df["risk_score"].mean(), 2))
    col4.metric("High Risk Count", int((result_df["risk_level"] == "High Risk").sum()))

    st.plotly_chart(
        px.histogram(result_df, x="risk_score", nbins=20, title="Risk Score Distribution"),
        use_container_width=True
    )

    st.plotly_chart(
        px.bar(
            result_df.groupby("type", as_index=False)["prediction"].sum(),
            x="type", y="prediction",
            title="Predicted Fraud Count by Transaction Type"
        ),
        use_container_width=True
    )

    st.plotly_chart(
        px.box(result_df, x="risk_level", y="amount", title="Amount Distribution by Risk Level"),
        use_container_width=True
    )

elif page == "Compliance Q&A":
    st.subheader("RAG-Style Compliance Assistant")
    st.write("Ask questions about AML, KYC, fraud policy, suspicious transactions, or investigation rules.")

    question = st.text_input("Ask your compliance question", value="Why should high amount cash out transactions be reviewed?")
    if st.button("Get Answer"):
        answer = answer_policy_question(question)
        st.text_area("Answer", answer, height=260)

elif page == "Generate Report":
    st.subheader("Generate Fraud Investigation PDF Report")

    if "result_df" in st.session_state:
        result_df = st.session_state["result_df"]
    else:
        result_df = predict_transactions(pd.read_csv(DATA_PATH))

    high_risk_df = result_df.sort_values("risk_score", ascending=False)
    tx_options = high_risk_df["transaction_id"].astype(str).tolist()
    selected_tx = st.selectbox("Select Transaction", tx_options)

    row = high_risk_df[high_risk_df["transaction_id"].astype(str) == selected_tx].iloc[0]
    explanation = explain_transaction(row)

    st.write("Selected Transaction")
    st.dataframe(pd.DataFrame([row]), use_container_width=True)
    st.write("Explanation")
    st.write(explanation)

    if st.button("Generate PDF Report"):
        report_path = generate_report(row, explanation)
        st.success(f"Report generated: {report_path.name}")
        with open(report_path, "rb") as f:
            st.download_button(
                "Download PDF Report",
                data=f,
                file_name=report_path.name,
                mime="application/pdf"
            )

elif page == "Model Metrics":
    st.subheader("Model Performance Metrics")

    if not METRICS_PATH.exists():
        metrics = train_model()
    else:
        metrics = json.loads(METRICS_PATH.read_text(encoding="utf-8"))

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Accuracy", metrics["accuracy"])
    col2.metric("Precision", metrics["precision"])
    col3.metric("Recall", metrics["recall"])
    col4.metric("F1 Score", metrics["f1_score"])

    st.write("Confusion Matrix")
    st.dataframe(pd.DataFrame(metrics["confusion_matrix"], columns=["Predicted Normal", "Predicted Fraud"], index=["Actual Normal", "Actual Fraud"]))
