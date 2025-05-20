import pandas as pd
from price_lookup import get_online_prices

def compare_prices(items, serpapi_key):
    results = []
    for item in items:
        part_number = item.get("part_number")
        manufacturer = item.get("manufacturer")
        quoted_price = item.get("quoted_price")
        best_price, avg_price, urls = get_online_prices(part_number, manufacturer, serpapi_key)
        results.append({
            "Part Number": part_number,
            "Manufacturer": manufacturer,
            "Quoted Price": quoted_price,
            "Best Online Price": best_price,
            "Average Online Price": avg_price,
            "Sources": ", ".join(urls) if urls else "N/A"
        })
    return pd.DataFrame(results)
