import unittest
from .calculator import calculate_mean_price, calculate_stock_profit, calculate_portfolio_profit_in_percentage, \
    calculate_profit_in_percentage, calculate_total_amount_invested


class CalculateTest(unittest.TestCase):

    def test_profit_calculation(self):
        self.assertEqual(calculate_stock_profit(150, 160, 20), 200)

    def test_total_amount_invested(self):
        self.assertEqual(calculate_total_amount_invested(180, 10), 1800)

    def test_total_amount_invested_empty(self):
        self.assertEqual(calculate_total_amount_invested(0, 0), 0)

    def test_portfolio_total_amount_invested_empty(self):
        self.assertEqual(calculate_portfolio_profit_in_percentage(4000, 400), 10)

    def test_mean_price(self):
        self.assertEqual(
            calculate_mean_price([339000, 385000, 325000, 259000, 397500, 325000, 285000, 545000, 359500, 775000]),
            399500.0)

    def test_calculate_profit_in_percentage(self):
        self.assertEqual(calculate_profit_in_percentage(200, 10, 200), 10.0)


if __name__ == '__main__':
    unittest.main()
