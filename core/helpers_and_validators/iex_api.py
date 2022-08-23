import requests
import os

import sentry_sdk
from decouple import config

BASE_URL = 'https://cloud.iexapis.com/v1/'
API_KEY = os.getenv("IEXCLOUD_API_KEY", config("IEXCLOUD_API_KEY"))


def check_active_connection():
    try:
        response = requests.get(
            f'https://cloud.iexapis.com/stable/stock/aapl/quote?token={API_KEY}').json()
        return True
    except ConnectionError as e:
        sentry_sdk.capture_exception(e)
        return False
    except IndexError as e:
        sentry_sdk.capture_exception(e)
        return False


class IexCloudAPI:
    """
    IEX Cloud class to get stock data
    """

    def __init__(self, stock_symbol):
        self.user_input_symbol = stock_symbol
        self.base_url = BASE_URL
        self.api_key = API_KEY
        self.active_connection = check_active_connection()
        self.stock_json = self.get_stock_package(stock_symbol)
        self.stock_symbol = self.get_stock_symbol_name()
        self.latest_stock_price = self.get_stock_price()

    def get_stock_package(self, user_input_stock_symbol: str):
        """
        @param user_input_stock_symbol: string
        @return: Stock json object
        """
        if self.active_connection:
            try:
                response = requests.get(
                    f'https://cloud.iexapis.com/stable/stock/{user_input_stock_symbol}/quote?token={API_KEY}').json()
                self.stock_json = response
                return response
            except ConnectionError as e:
                sentry_sdk.capture_exception(e)
            except IndexError as e:
                sentry_sdk.capture_exception(e)
        else:
            return self.stock_json

    def get_stock_symbol_name(self):
        """
        @return: Symbol name: string
        """
        return self.stock_json['symbol']

    def get_stock_price(self):
        """
        @return: Latest stock price: float
        """
        if not self.stock_json:
            self.get_stock_package(self.stock_symbol)
            return self.stock_json['latestPrice']
        else:
            return self.stock_json['latestPrice']
