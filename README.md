# AI-Powered FinTech Fraud Risk & Compliance Assistant

## Live App

https://fintech-genai-fraud-risk-assistant-anand.streamlit.app/


This is an advanced LLM / GenAI FinTech project for fraud detection, risk explanation, compliance Q&A, dashboard analytics, and PDF report generation.

## Features

- Fraud detection using Machine Learning
- Risk score and fraud probability
- GenAI-style explanation for suspicious transactions
- RAG-style compliance Q&A from policy documents
- Fraud analytics dashboard
- PDF fraud investigation report
- Ready-to-run Streamlit app

## Tech Stack

- Python
- Streamlit
- Scikit-learn
- Pandas
- Plotly
- FPDF

## How to Run

### Step 1: Extract ZIP

Extract this folder anywhere on your computer.

### Step 2: Open Terminal in Project Folder

```bash
cd fintech-genai-fraud-risk-assistant
```

### Step 3: Create Virtual Environment

For Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

For Mac/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 4: Install Requirements

```bash
pip install -r requirements.txt
```

### Step 5: Train Model

```bash
python src/train_model.py
```

### Step 6: Run App

```bash
streamlit run app.py
```

Then open the local URL shown in terminal.

## One-Line Windows Command

```powershell
python -m venv .venv; .venv\Scripts\Activate.ps1; pip install -r requirements.txt; python src/train_model.py; streamlit run app.py
```

## Dataset

The project includes a sample synthetic transaction dataset:

```text
data/sample_transactions.csv
```

Important columns:

- transaction_id
- type
- amount
- oldbalanceOrg
- newbalanceOrig
- oldbalanceDest
- newbalanceDest
- hour
- location
- isFraud

## Resume Description

**AI-Powered FinTech Fraud Risk & Compliance Assistant**  
Built an advanced GenAI-based fintech system using Python, Streamlit, Machine Learning, and RAG-style document retrieval to detect suspicious financial transactions, explain fraud risk, answer compliance-related questions, and generate fraud investigation reports.

## GitHub Repository Name

```text
fintech-genai-fraud-risk-assistant
```

## LinkedIn Short Description

Built an AI-powered FinTech fraud risk assistant using Machine Learning, Streamlit, and GenAI-style explanations. The project detects suspicious financial transactions, provides risk scores, answers compliance questions from policy documents, and generates fraud investigation reports.
