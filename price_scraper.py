
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/58.0.3029.110 Safari/537.3"
}

def extract_prices_amazon(search_term):
    url = f"https://www.amazon.com/s?k={'+'.join(search_term.split())}"
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    prices = []
    links = []
    for div in soup.find_all("div", {"data-component-type": "s-search-result"}):
        price_whole = div.select_one("span.a-price > span.a-offscreen")
        link = div.select_one("a.a-link-normal.a-text-normal")
        if price_whole and link:
            try:
                price = float(re.sub(r'[^\d.]', '', price_whole.text.strip()))
                prices.append(price)
                links.append("https://www.amazon.com" + link['href'])
            except:
                continue
        if len(prices) >= 5:
            break
    return prices, links

def extract_prices_digikey(search_term):
    url = f"https://www.digikey.com/en/products/result?s={'+'.join(search_term.split())}"
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    prices = []
    links = []
    for row in soup.find_all("tr", {"class": "MuiTableRow-root"}):
        price_cell = row.find("td", {"class": "MuiTableCell-root MuiTableCell-body"})
        link_tag = row.find("a", href=True)
        if price_cell and link_tag:
            try:
                price = float(re.sub(r'[^\d.]', '', price_cell.text.strip()))
                prices.append(price)
                links.append("https://www.digikey.com" + link_tag['href'])
            except:
                continue
        if len(prices) >= 5:
            break
    return prices, links

def scrape_prices(df):
    results = []
    for _, row in df.iterrows():
        part = row["Part Number"]
        mfg = row["Manufacturer"]
        search_term = f"{mfg} {part}"

        amazon_prices, amazon_links = extract_prices_amazon(search_term)
        digikey_prices, digikey_links = extract_prices_digikey(search_term)

        all_prices = amazon_prices + digikey_prices
        all_links = amazon_links + digikey_links

        if all_prices:
            best_price = min(all_prices)
            avg_price = sum(all_prices) / len(all_prices)
            best_source = all_links[all_prices.index(best_price)] if best_price in all_prices else "N/A"
            sources_summary = "; ".join(all_links[:3])
        else:
            best_price = avg_price = 0.0
            best_source = sources_summary = "No data"

        results.append({
            "Part Number": part,
            "Manufacturer": mfg,
            "Best Online Price": round(best_price, 2),
            "Average Online Price": round(avg_price, 2),
            "Best Price Source": best_source,
            "Avg Price Sources": sources_summary
        })

        time.sleep(1)  # polite delay
    return pd.DataFrame(results)
