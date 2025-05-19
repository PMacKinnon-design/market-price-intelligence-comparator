
import os
import requests
import pandas as pd
import time

SERPAPI_KEY = os.getenv("SERPAPI_API_KEY") or "YOUR_PRIVATE_KEY_HERE"

def get_prices_via_serpapi(query):
    params = {
        "engine": "google_shopping",
        "q": query,
        "api_key": SERPAPI_KEY,
    }
    response = requests.get("https://serpapi.com/search", params=params)
    data = response.json()

    prices = []
    links = []

    if "shopping_results" in data:
        for result in data["shopping_results"][:5]:  # Limit to top 5
            price_str = result.get("price", "")
            link = result.get("link", "")
            try:
                price = float(price_str.replace("$", "").replace(",", ""))
                prices.append(price)
                links.append(link)
            except:
                continue

    return prices, links

def scrape_prices(df):
    results = []
    for _, row in df.iterrows():
        part = row["Part Number"]
        mfg = row["Manufacturer"]
        search_term = f"{mfg} {part}"

        prices, links = get_prices_via_serpapi(search_term)

        if prices:
            best_price = min(prices)
            avg_price = sum(prices) / len(prices)
            best_source = links[prices.index(best_price)] if best_price in prices else "N/A"
            sources_summary = "; ".join(links[:3])
        else:
            best_price = avg_price = 0.0
            best_source = sources_summary = "No data found"

        results.append({
            "Part Number": part,
            "Manufacturer": mfg,
            "Best Online Price": round(best_price, 2),
            "Average Online Price": round(avg_price, 2),
            "Best Price Source": best_source,
            "Avg Price Sources": sources_summary
        })

        time.sleep(1)  # Be respectful of API usage
    return pd.DataFrame(results)
