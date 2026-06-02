from pathlib import Path
from fpdf import FPDF
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = ROOT / "reports"

def generate_report(row, explanation):
    REPORTS_DIR.mkdir(exist_ok=True)
    tx_id = str(row.get("transaction_id", "transaction"))
    filename = REPORTS_DIR / f"fraud_report_{tx_id}.pdf"

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(0, 10, "AI-Powered FinTech Fraud Investigation Report", ln=True)

    pdf.set_font("Arial", size=11)
    pdf.ln(5)
    pdf.cell(0, 8, f"Generated On: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.cell(0, 8, f"Transaction ID: {tx_id}", ln=True)
    pdf.cell(0, 8, f"Transaction Type: {row.get('type', '')}", ln=True)
    pdf.cell(0, 8, f"Amount: {row.get('amount', '')}", ln=True)
    pdf.cell(0, 8, f"Location: {row.get('location', '')}", ln=True)
    pdf.cell(0, 8, f"Risk Score: {row.get('risk_score', '')}", ln=True)
    pdf.cell(0, 8, f"Risk Level: {row.get('risk_level', '')}", ln=True)

    pdf.ln(5)
    pdf.multi_cell(0, 8, "AI Explanation:")
    pdf.multi_cell(0, 8, str(explanation))

    pdf.ln(5)
    pdf.multi_cell(0, 8, "Recommended Compliance Action:")
    pdf.multi_cell(0, 8, "Review high-risk transactions manually, verify customer identity if required, and document analyst decision.")

    pdf.output(str(filename))
    return filename
