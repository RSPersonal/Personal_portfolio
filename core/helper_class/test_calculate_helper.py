import unittest
from .CalculateHelper import *


class CalculateTest(unittest.TestCase):

    def test_profit_calculation(self):
        self.assertEqual(calculate_stock_profit(150, 160, 20), 200)

    def test_total_amount_invested(self):
        self.assertEqual(calculate_total_amount_invested(180, 10), 1800)

    def test_total_amount_invested_empty(self):
        self.assertEqual(calculate_total_amount_invested(0, 0), 0)

    def test_portfolio_total_amount_invested_empty(self):
        self.assertEqual(calculate_portfolio_profit_in_percentage(4000, 400), 10)


if __name__ == '__main__':
    unittest.main(argv=['', '-v'])
