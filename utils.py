import pandas as pd

def evaluate_risks(contract_text, risk_rules):
    results = []
    for rule in risk_rules:
        if rule["keyword"].lower() in contract_text.lower():
            results.append({
                "Clause": rule["keyword"],
                "Risk Category": rule["category"],
                "Severity": rule["severity"],
                "Recommended Action": rule["action"],
                "Suggested Flowdown": rule["flowdown"]
            })
    return pd.DataFrame(results)

def generate_flowdowns(risk_df):
    if risk_df.empty:
        return pd.DataFrame(columns=["Clause", "Suggested Flowdown"])
    return risk_df[["Clause", "Suggested Flowdown"]]