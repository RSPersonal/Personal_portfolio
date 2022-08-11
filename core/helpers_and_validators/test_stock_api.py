import unittest
from .stock_api import test_api_connection, get_stock_price, get_stock_ticker_symbol


class TestStockApi(unittest.TestCase):

    def test_stock_api_connection(self):
        self.assertEqual(test_api_connection(), True)

    def test_stock_api_get_stock_price(self):
        self.assertIsInstance(get_stock_price('AAPL'), float)

    def test_stock_api_get_stock_ticker_symbol(self):
        self.assertEqual(get_stock_ticker_symbol('AAPL'), 'AAPL')


if __name__ == '__main__':
    unittest.main()
