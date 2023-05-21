import json
import requests

def investment_lookup(symbol, quantity):

    # Make a request to the Alpha Vantage API to search for name based on the symbol
    api_key = "M2BV5Y064JE1OM8H"
    url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={symbol}&apikey={api_key}"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return None
        data = json.loads(response.text)
        best_match = data.get("bestMatches", [])
        if len(best_match) > 0:
            name = best_match[0].get("2. name")
    except requests.RequestException:
        return None

    # Make a request to the Alpha Vantage API and parse the JSON response to get the current price of the investment
    api_key = "LS80WTP12NGATLQX"
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={api_key}"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return None
        data = json.loads(response.text)
    except requests.RequestException:
        return None
    # Find the most recent day and extract the current price from that day
    if "Time Series (Daily)" in data:
        for day, values in data["Time Series (Daily)"].items():
            price = float(values["1. open"])
    else:
        return None

    value = float(quantity) * price

    return {
            "symbol": symbol,
            "quantity": quantity,
            "name": name,
            "price": price,
            "value": value,
        }
