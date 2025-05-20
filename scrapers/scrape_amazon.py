
import requests
from bs4 import BeautifulSoup

def scrape_amazon_prices(part_number):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    }
    search_url = f"https://www.amazon.com/s?k={part_number.replace(' ', '+')}"
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    results = []
    items = soup.select(".s-result-item")
    for item in items[:5]:
        title = item.select_one("h2 span")
        price_whole = item.select_one(".a-price-whole")
        price_fraction = item.select_one(".a-price-fraction")
        link = item.select_one("h2 a")
        
        if title and price_whole and link:
            price = float(price_whole.text.replace(",", "") + "." + (price_fraction.text if price_fraction else "00"))
            results.append({
                "Source": "Amazon",
                "Title": title.text.strip(),
                "Price": price,
                "Link": "https://www.amazon.com" + link.get("href")
            })
    return results
