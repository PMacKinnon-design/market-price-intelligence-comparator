import requests

def get_online_prices(part_number, manufacturer, serpapi_key):
    try:
        query = f"{manufacturer} {part_number} buy"
        params = {
            "engine": "google",
            "q": query,
            "api_key": serpapi_key,
            "num": 5
        }
        response = requests.get("https://serpapi.com/search", params=params)
        data = response.json()

        prices = []
        urls = []

        for result in data.get("shopping_results", []):
            price = result.get("price")
            link = result.get("link")
            if price:
                price = float(str(price).replace("$", "").replace(",", "").strip())
                prices.append(price)
                urls.append(link)

        best_price = min(prices) if prices else None
        avg_price = sum(prices) / len(prices) if prices else None
        return best_price, avg_price, urls
    except Exception as e:
        return None, None, []
