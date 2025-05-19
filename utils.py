
import pandas as pd

def compare_with_market(user_df, market_df):
    merged = pd.merge(user_df, market_df, on=["Part Number", "Manufacturer"], how="left")
    merged["Price Delta (Best)"] = merged["Price Paid"] - merged["Best Online Price"]
    merged["Potential Savings"] = merged.apply(
        lambda x: (x["Price Delta (Best)"] * x["Quantity"]) if x["Price Delta (Best)"] > 0 else 0, axis=1
    )
    return merged[[
        "Part Number", "Manufacturer", "Description", "Quantity", "Price Paid",
        "Best Online Price", "Average Online Price", "Price Delta (Best)",
        "Potential Savings", "Best Price Source", "Avg Price Sources"
    ]]
