import requests
from pprint import pprint


def get_data(symbol):
    api_key = "M2BV5Y064JE1OM8H"
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey=demo{api_key}"

    try:
        r = requests.get(url)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Error making API request:", e)
        return None

    data = r.json()

    if 'Time Series (Daily)' not in data:
        print("Error: No daily data found")
        return None

    daily_data = data['Time Series (Daily)']
    return daily_data


symbol = input("Enter symbol (for example: IBM): ")
daily_data = get_data(symbol)

if daily_data:
    for date, stock_data in list(daily_data.items())[:5]:
        pprint(f'{date}: {stock_data}')

# url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={keyword}&apikey={api_key}'
# r = requests.get(url)
# data = r.json()
