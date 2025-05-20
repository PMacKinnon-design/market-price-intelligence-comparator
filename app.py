import streamlit as st
import pandas as pd
from utils import compare_prices
from price_lookup import get_online_prices

# Sidebar for API key
st.sidebar.header("Configuration")
serpapi_key = st.sidebar.text_input("Enter your SerpApi API Key", type="password")

st.title("Market Price Intelligence Comparator")

input_method = st.radio("Choose input method", ["Manual Entry", "Upload CSV"])

items = []

if input_method == "Manual Entry":
    num_items = st.number_input("How many items do you want to compare?", min_value=1, max_value=5, value=1)
    for i in range(num_items):
        part_number = st.text_input(f"Part Number {i+1}")
        manufacturer = st.text_input(f"Manufacturer {i+1}")
        quoted_price = st.number_input(f"Quoted Price {i+1}", min_value=0.0, value=0.0)
        items.append({"part_number": part_number, "manufacturer": manufacturer, "quoted_price": quoted_price})
elif input_method == "Upload CSV":
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        items = df.to_dict(orient="records")

if items and serpapi_key:
    comparison_df = compare_prices(items, serpapi_key)
    st.dataframe(comparison_df)
elif items:
    st.warning("Please enter your SerpApi API key in the sidebar to enable real-time price scraping.")
