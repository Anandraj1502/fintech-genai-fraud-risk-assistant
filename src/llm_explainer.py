def explain_transaction(row):
    reasons = []

    amount = float(row.get("amount", 0))
    tx_type = str(row.get("type", "UNKNOWN"))
    hour = int(row.get("hour", 12))
    old_balance = float(row.get("oldbalanceOrg", 0))
    new_balance = float(row.get("newbalanceOrig", 0))
    risk_score = float(row.get("risk_score", 0))

    if amount > 45000:
        reasons.append("transaction amount is unusually high")
    if tx_type in ["TRANSFER", "CASH_OUT"]:
        reasons.append(f"transaction type is {tx_type}, which is more sensitive in fraud monitoring")
    if hour <= 4:
        reasons.append("transaction happened during late-night hours")
    if old_balance > 0 and amount / old_balance > 0.75:
        reasons.append("transaction amount consumes a large portion of the sender balance")
    if new_balance == 0:
        reasons.append("sender balance becomes zero after the transaction")

    if not reasons:
        reasons.append("transaction pattern is mostly consistent with normal behavior")

    explanation = (
        f"This transaction has a risk score of {risk_score:.2f}/100. "
        f"It is flagged because " + ", ".join(reasons) + "."
    )

    if risk_score >= 70:
        action = "Recommended action: hold transaction for manual review and verify customer identity."
    elif risk_score >= 40:
        action = "Recommended action: monitor the transaction and review customer history."
    else:
        action = "Recommended action: no immediate action required, but keep it in monitoring logs."

    return explanation + " " + action
