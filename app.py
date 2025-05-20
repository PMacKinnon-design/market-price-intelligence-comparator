import streamlit as st
import json
from utils import evaluate_risks, generate_flowdowns

st.set_page_config(page_title="AI Contract Risk Review & Flowdown Generator", layout="wide")

st.title("📜 AI Contract Risk Review & Flowdown Generator")

uploaded_file = st.file_uploader("Upload a Contract (.txt file)", type="txt")

if uploaded_file:
    contract_text = uploaded_file.read().decode("utf-8")
    st.subheader("Contract Text")
    st.text_area("Contents", contract_text, height=300)

    with open("data/risk_rules.json") as f:
        risk_rules = json.load(f)

    result_df = evaluate_risks(contract_text, risk_rules)
    st.subheader("🛡️ Risk Evaluation Results")
    st.dataframe(result_df, use_container_width=True)

    flowdown_df = generate_flowdowns(result_df)
    st.subheader("🔁 Flowdown Clauses")
    st.dataframe(flowdown_df, use_container_width=True)

    csv = flowdown_df.to_csv(index=False).encode("utf-8")
    st.download_button("Download Flowdown Clauses as CSV", data=csv, file_name="flowdown_clauses.csv", mime="text/csv")