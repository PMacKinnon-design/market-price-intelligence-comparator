import pandas as pd
import random
import matplotlib.pyplot as plt
import streamlit as st

# Simulated online price fetching
def fetch_online_prices(df):
    results = []
    for _, row in df.iterrows():
        part = row.get("Part Number", "Unknown")
        manu = row.get("Manufacturer", "Unknown")
        best_price = round(random.uniform(10, 100), 2)
        avg_price = round(best_price + random.uniform(5, 20), 2)
        results.append({
            "Part Number": part,
            "Manufacturer": manu,
            "Best Price (USD)": best_price,
            "Average Price (USD)": avg_price,
            "Reference URL": f"https://example.com/search?q={part}+{manu}"
        })
    return pd.DataFrame(results)

def visualize_prices(df):
    if df.empty:
        st.info("No data to visualize.")
        return

    fig, ax = plt.subplots()
    df.plot.bar(x="Part Number", y=["Best Price (USD)", "Average Price (USD)"], ax=ax)
    st.pyplot(fig)