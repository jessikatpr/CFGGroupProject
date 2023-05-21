import unittest
from Investment import Investment, Bond

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


if __name__ == '__main__':
    unittest.main()
