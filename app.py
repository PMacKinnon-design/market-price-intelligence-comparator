import streamlit as st
import pandas as pd
from utils import fetch_online_prices, visualize_prices

st.set_page_config(page_title="Market Price Intelligence Comparator", layout="wide")

st.title("📊 Market Price Intelligence Comparator")

# Manual Entry
st.header("Manual Entry")
manual_data = []
for i in range(5):
    part_number = st.text_input(f"Part Number {i+1}", key=f"part_{i}")
    manufacturer = st.text_input(f"Manufacturer {i+1}", key=f"manu_{i}")
    if part_number and manufacturer:
        manual_data.append({"Part Number": part_number, "Manufacturer": manufacturer})

# File Upload
st.header("Upload Excel or CSV File")
uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx"])
if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            file_data = pd.read_csv(uploaded_file)
        else:
            file_data = pd.read_excel(uploaded_file)
        st.success("File uploaded successfully.")
    except Exception as e:
        st.error(f"Error reading file: {e}")
        file_data = pd.DataFrame()
else:
    file_data = pd.DataFrame()

# Combine manual and file data
all_data = pd.DataFrame(manual_data)
if not file_data.empty:
    all_data = pd.concat([all_data, file_data], ignore_index=True)

if not all_data.empty:
    st.subheader("Input Data")
    st.dataframe(all_data)

    st.subheader("Comparative Pricing Results")
    result_df = fetch_online_prices(all_data)
    st.dataframe(result_df)

    st.subheader("Visual Comparison")
    visualize_prices(result_df)