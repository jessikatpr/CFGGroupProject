import requests
import json
import decimal


class Investment:
    def __init__(self, symbol, name, quantity, purchase_price):
        self.symbol = symbol
        self.name = name
        self.quantity = quantity
        self.purchase_price = purchase_price

    def current_price(self):
        """Get the current price of the investment from the financial API"""
        # Make a request to the Alpha Vantage API and parse the JSON response
        api_key = "MUBEJZKSC659866J"
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={self.symbol}&apikey={api_key}"
        response = requests.get(url)
        data = json.loads(response.text)

        # Find the most recent week and extract the current price from that week
        if "Weekly Time Series" in data:
            for week, values in data["Weekly Time Series"].items():
                price = values["1. open"]
                break
        else:
            price = 0

        return decimal.Decimal(price)

    def current_value(self):
        """Calculate the current value of the investment"""
        price = self.current_price()
        value = price * decimal.Decimal(self.quantity)
        return value


class Stock(Investment):
    def __init__(self, symbol, name, quantity, purchase_price):
        super().__init__(symbol, name, quantity, purchase_price)
        self.type = "stock"


class Portfolio:
    def __init__(self):
        self.investments = []

    def add_investment(self, investment):
        self.investments.append(investment)

    def remove_investment(self, investment):
        self.investments.remove(investment)

    def total_value(self):
        """Calculate the total value of the portfolio"""
        total_value = decimal.Decimal(0)
        for investment in self.investments:
            total_value += investment.current_value()
        return total_value

    def display(self):
        """Display the portfolio data"""
        print("Investment Portfolio:")
        print("=====================")
        total_value = decimal.Decimal(0)
        for investment in self.investments:
            print(f"{investment.type} - {investment.name} ({investment.symbol}):")
            print(f"\tQuantity: {investment.quantity}")
            print(f"\tPurchase Price: {investment.purchase_price}")
            current_price = investment.current_price()
            current_value = investment.current_value()
            print(f"\tCurrent Price: {current_price:.2f}")
            print(f"\tCurrent Value: {current_value:.2f}")
            total_value += current_value
            print("")
        print(f"Total Portfolio Value: {total_value:.2f}")


def run():
    # Create an empty portfolio
    portfolio = Portfolio()

    # Add investments to the portfolio
    stock1 = Stock("AAPL", "Apple Inc.", 100, 130.00)
    portfolio.add_investment(stock1)

    stock2 = Stock("ABNB", "Airbnb", 50, 99.00)
    portfolio.add_investment(stock2)


    portfolio.display()


if __name__ == '__main__':
    run()