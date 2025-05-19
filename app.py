
import streamlit as st
import pandas as pd
from utils import compare_with_market
from price_scraper import scrape_prices
import matplotlib.pyplot as plt

st.set_page_config(page_title="Market Price Intelligence Comparator", layout="wide")
st.title("📊 Market Price Intelligence Comparator")

st.markdown("Enter a few items manually or upload a quote (Excel/CSV) to compare against live market pricing.")

# Manual entry
with st.expander("🔘 Enter Item Manually"):
    with st.form("manual_entry"):
        part_number = st.text_input("Part Number")
        manufacturer = st.text_input("Manufacturer")
        description = st.text_input("Description")
        quantity = st.number_input("Quantity", min_value=1, value=1)
        price_paid = st.number_input("Unit Price Paid ($)", min_value=0.0, value=0.0, step=0.01)
        submitted = st.form_submit_button("Compare")
        if submitted:
            user_item = pd.DataFrame([{
                "Part Number": part_number,
                "Manufacturer": manufacturer,
                "Description": description,
                "Quantity": quantity,
                "Price Paid": price_paid
            }])
            market_data = scrape_prices(user_item)
            result = compare_with_market(user_item, market_data)
            st.dataframe(result)
            st.bar_chart(result[["Price Paid", "Best Online Price", "Average Online Price"]].T)

# File upload
st.divider()
upload_file = st.file_uploader("📂 Upload Quote (Excel or CSV)", type=["csv", "xlsx"])
if upload_file:
    if upload_file.name.endswith("csv"):
        user_df = pd.read_csv(upload_file)
    else:
        user_df = pd.read_excel(upload_file)
    st.success("File uploaded. Searching market prices...")
    market_df = scrape_prices(user_df)
    result_df = compare_with_market(user_df, market_df)
    st.dataframe(result_df)
    st.download_button("Download Full Report", result_df.to_csv(index=False), "market_price_comparison.csv", "text/csv")
