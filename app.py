
import streamlit as st
import pandas as pd
import os
from scrapers.scrape_amazon import scrape_amazon_prices
from utils import parse_uploaded_file

st.set_page_config(page_title="Market Price Intelligence Comparator", layout="wide")

st.title("Market Price Intelligence Comparator")
st.markdown("Compare your pricing data with real-time online benchmarks.")

# Input method selection
input_method = st.radio("Select input method:", ["Manual Entry", "Upload CSV/Excel File"])

if input_method == "Manual Entry":
    st.subheader("Enter Part Details")
    with st.form("manual_form"):
        part_number = st.text_input("Part Number")
        manufacturer = st.text_input("Manufacturer")
        description = st.text_input("Description")
        quoted_price = st.number_input("Quoted Price", min_value=0.0, step=0.01)
        submitted = st.form_submit_button("Compare")
        if submitted and part_number:
            st.write("Fetching online prices...")
            online_data = scrape_amazon_prices(part_number)
            df = pd.DataFrame(online_data)
            df["Quoted Price"] = quoted_price
            st.dataframe(df)
            st.bar_chart(df.set_index("Source")[["Price"]])

elif input_method == "Upload CSV/Excel File":
    uploaded_file = st.file_uploader("Upload CSV or Excel file with part numbers", type=["csv", "xlsx"])
    if uploaded_file:
        items_df = parse_uploaded_file(uploaded_file)
        st.write("Uploaded Data", items_df)
        results = []
        for _, row in items_df.iterrows():
            online_data = scrape_amazon_prices(row["Part Number"])
            for entry in online_data:
                entry["Part Number"] = row["Part Number"]
                entry["Quoted Price"] = row["Quoted Price"]
            results.extend(online_data)
        results_df = pd.DataFrame(results)
        st.dataframe(results_df)
