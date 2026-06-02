from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "documents"

def load_documents():
    docs = []
    for path in DOCS_DIR.glob("*.txt"):
        docs.append({
            "source": path.name,
            "content": path.read_text(encoding="utf-8")
        })
    return docs

def answer_policy_question(question: str):
    docs = load_documents()
    question_words = set(re.findall(r"\w+", question.lower()))

    scored = []
    for doc in docs:
        content_words = set(re.findall(r"\w+", doc["content"].lower()))
        score = len(question_words.intersection(content_words))
        scored.append((score, doc))

    scored.sort(key=lambda x: x[0], reverse=True)
    best_score, best_doc = scored[0]

    if best_score == 0:
        return (
            "I could not find a strong policy match. "
            "Try asking about AML, KYC, fraud investigation, suspicious transaction, high amount, or compliance review."
        )

    return (
        f"Based on {best_doc['source']}:\n\n"
        f"{best_doc['content']}\n\n"
        f"Answer: For this question, the most relevant policy point is that suspicious or unusual financial activity should be reviewed using risk indicators, customer behavior, and compliance rules."
    )
