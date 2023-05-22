import unittest
from Investment import Investment, Bond, Stock, Portfolio, MutualFund
from unittest.mock import patch


class TestInvestment(unittest.TestCase):
    def test_investment(self):
        symbol = "APPL"
        name = "Apple Inc."
        quantity = 10
        purchase_price = 130.0
        investment = Investment(symbol, name, quantity, purchase_price)

        self.assertEqual(investment.symbol, symbol)
        self.assertEqual(investment.name, name)
        self.assertEqual(investment.quantity, quantity)
        self.assertEqual(investment.purchase_price, purchase_price)

    def test_bond(self):
        symbol = "TSLA"
        name = "Tesla Inc."
        quantity = 50
        purchase_price = 1000.0
        coupon_rate = 0.05
        bond = Bond(symbol, name, quantity, purchase_price, coupon_rate)

        self.assertEqual(bond.symbol, symbol)
        self.assertEqual(bond.name, name)
        self.assertEqual(bond.quantity, quantity)
        self.assertEqual(bond.purchase_price, purchase_price)
        self.assertEqual(bond.type, "bond")
        self.assertEqual(bond.coupon_rate, coupon_rate)

    def test_stock(self):
        symbol = "TSLA"
        name = "Tesla Inc."
        quantity = 50
        purchase_price = 1000.0
        stock = Stock(symbol, name, quantity, purchase_price)

        self.assertEqual(stock.symbol, symbol)
        self.assertEqual(stock.name, name)
        self.assertEqual(stock.quantity, quantity)
        self.assertEqual(stock.purchase_price, purchase_price)
        self.assertEqual(stock.type, "stock")

    def test_mutualfund(self):
        symbol = "TSLA"
        name = "Tesla Inc."
        quantity = 50
        purchase_price = 1000.0
        expense_ratio = 0.05
        mutualfund = MutualFund(symbol, name, quantity, purchase_price, expense_ratio)

        self.assertEqual(mutualfund.symbol, symbol)
        self.assertEqual(mutualfund.name, name)
        self.assertEqual(mutualfund.quantity, quantity)
        self.assertEqual(mutualfund.purchase_price, purchase_price)
        self.assertEqual(mutualfund.type, "mutual_fund")
        self.assertEqual(mutualfund.expense_ratio, expense_ratio)
        
    @patch('requests.get')
    def test_current_price(self, mock_get):
        symbol = "ABNB"
        name = "Airbnb"
        quantity = 5
        purchase_price = 110.0
        investment = Investment(symbol, name, quantity, purchase_price)

        # API response
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.text = '''{
            "Time Series (Daily)": {
                "2023-05-22": {
                    "1. open": "1234.12"
                }
            }
        }'''

        price = investment.current_price()

        # Price & mock value should match
        self.assertEqual(price, 1234.12)

    @patch('requests.get')
    def test_total_value(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.text = '''{
            "Time Series (Daily)": {
                "2023-05-22": {
                    "1. open": "1234.12"
                }
            }
        }'''

        # Create portfolio
        portfolio = Portfolio()
        stock = Stock("ABNB", "Airbnb", 5, 110.0)
        bond = Bond("APPL", "Tesla Inc", 10, 100, 0.1)

        # Add investments to portfolio
        portfolio.add_investment(stock)
        portfolio.add_investment(bond)

        # Check total value
        value = stock.current_value() + bond.current_value()
        self.assertEqual(portfolio.total_value(), value)


    # Testing invalid inputs
    def test_negative_quantity(self):
        with self.assertRaises(ValueError):
            Investment("ABNB", "Airbnb", -1, 100.00)

    def test_invalid_data_type(self):
        with self.assertRaises(ValueError):
            Investment("ABNB", "Airbnb", True, 100.00)


if __name__ == '__main__':
    unittest.main()
