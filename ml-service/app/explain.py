
def explain_score(features, credo_score, risk_band):
    reasons = []

    savings_rate = features["savings_rate"]
    expense_ratio = features["expense_to_income_ratio"]
    average_balance = features["average_balance"]

    if savings_rate >= 0.15:
        reasons.append("Positive savings rate")
    else:
        reasons.append("Low or negative savings rate")

    if expense_ratio <= 0.80:
        reasons.append("Expenses are relatively low compared with income")
    else:
        reasons.append("Expenses are high compared with income")

    if average_balance >= 5000:
        reasons.append("Average balance meets the prototype threshold")
    else:
        reasons.append("Average balance is below the prototype threshold")

    return {
        "credo_score": int(credo_score),
        "risk_band": risk_band,
        "reasons": reasons
    }
