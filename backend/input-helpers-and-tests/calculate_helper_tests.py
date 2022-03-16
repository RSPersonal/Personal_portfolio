import unittest
from CalculateHelper import calculate_stock_profit


class CalculateTest(unittest.TestCase):

    def test_profit_calculation(self):
        self.assertEqual(calculate_stock_profit(150, 160, 20), 200)


if __name__ == '__main__':
    unittest.main()
