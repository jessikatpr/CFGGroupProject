import json
import requests


class Investment:
    def __init__(self, symbol, name, quantity, purchase_price):
        self.symbol = symbol
        self.name = name
        self.quantity = quantity
        self.purchase_price = purchase_price
        self._current_price = None  # Store the current price

    def current_price(self):
        """Get the current price of the investment from the financial API"""
        if self._current_price is not None:
            return self._current_price

        # Make a request to the Alpha Vantage API and parse the JSON response
        api_key = "LS80WTP12NGATLQX"
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={self.symbol}&apikey={api_key}"
        try:
            response = requests.get(url)
            if response.status_code != 200:
                print(f"Error retrieving current price for {self.name} ({self.symbol}): {response.text}")
                return None
            data = json.loads(response.text)
        except requests.exceptions.RequestException as e:
            print(f"Error retrieving current price for {self.name} ({self.symbol}): {e}")
            return None

        # Find the most recent day and extract the current price from that day
        if "Time Series (Daily)" in data:
            for day, values in data["Time Series (Daily)"].items():
                price = float(values["1. open"])
                self._current_price = price  # Store the current price
                print(f"Current price for {self.name} ({self.symbol}): {price}")
                break
        else:
            price = None
            print(f"No price data found for {self.name} ({self.symbol})")

        return price

    def current_value(self):
        """Calculate the current value of the investment"""
        price = self.current_price()  # Use the stored current price
        if price:
            value = self.quantity * price
        else:
            value = 0
        return value

class Stock(Investment):
    def __init__(self, symbol, name, quantity, purchase_price):
        super().__init__(symbol, name, quantity, purchase_price)
        self.type = "stock"

class Bond(Investment):
    def __init__(self, symbol, name, quantity, purchase_price, coupon_rate):
        super().__init__(symbol, name, quantity, purchase_price)
        self.type = "bond"
        self.coupon_rate = coupon_rate

class MutualFund(Investment):
    def __init__(self, symbol, name, quantity, purchase_price, expense_ratio):
        super().__init__(symbol, name, quantity, purchase_price)
        self.type = "mutual_fund"
        self.expense_ratio = expense_ratio

class Portfolio:
    def __init__(self):
        self.investments = []

    def add_investment(self, investment):
        self.investments.append(investment)

    def remove_investment(self, investment):
        self.investments.remove(investment)

    def total_value(self):
        """Calculate the total value of the portfolio"""
        value = sum(investment.current_value() for investment in self.investments)
        return value


    def display(self):
        """Display the portfolio data"""
        print("Investment Portfolio:")
        print("=====================")
        for investment in self.investments:
            print(f"{investment.type} - {investment.name} ({investment.symbol}):")
            print(f"\tQuantity: {investment.quantity}")
            print(f"\tPurchase Price: {investment.purchase_price}")
            print(f"\tCurrent Price: {investment.current_price()}")
            print(f"\tCurrent Value: {investment.current_value()}")
            if isinstance(investment, Bond):
                print(f"\tCoupon Rate: {investment.coupon_rate}")
            elif isinstance(investment, MutualFund):
                print(f"\tExpense Ratio: {investment.expense_ratio}")
            print("")

        print(f"Total Portfolio Value: {self.total_value()}")

def run():
    # Create an empty portfolio
    portfolio = Portfolio()

    # Add investments to the portfolio
    stock1 = Stock("AAPL", "Apple Inc.", 100, 130.00)
    portfolio.add_investment(stock1)

    bond1 = Bond("TSLA", "Tesla Inc.", 50, 1000.00, 0.05)
    portfolio.add_investment(bond1)

    mutual_fund1 = MutualFund("SPY", "SPDR S&P 500 ETF Trust", 200, 350.00, 0.01)
    portfolio.add_investment(mutual_fund1)

    portfolio.display()

    print(stock1.current_price())

if __name__ == '__main__':
    run()

