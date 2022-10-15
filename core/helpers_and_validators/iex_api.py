import requests
import os
import json
import sentry_sdk
from decouple import config

BASE_URL = 'https://cloud.iexapis.com/v1/'
API_KEY = os.getenv("IEXCLOUD_API_KEY", config("IEXCLOUD_API_KEY"))


def check_active_connection() -> bool:
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
    base_url = BASE_URL

    def __init__(self, stock_symbol):
        self.user_input_symbol = stock_symbol
        self.api_key: str = API_KEY
        self.active_connection: bool = check_active_connection()
        self.valid_stock: bool = False
        self.stock_json = self.get_stock_package(stock_symbol)
        self.stock_symbol: str = self.get_stock_symbol_name()
        self.latest_stock_price: float | int = self.get_stock_price()
        self.error = None

    def get_stock_package(self, user_input_stock_symbol: str):
        """
        @param user_input_stock_symbol: string
        @return: Stock json object
        """
        if self.active_connection:
            try:
                response = requests.get(
                    f"https://cloud.iexapis.com/stable/stock/{user_input_stock_symbol}/quote?token={API_KEY}")
                if response:
                    self.valid_stock = True
                    self.stock_json = response.json()
                    return self.stock_json
            except ConnectionError as e:
                sentry_sdk.capture_exception(e)
                self.error = e
            except IndexError as e:
                sentry_sdk.capture_exception(e)
                self.error = e

    def get_stock_symbol_name(self) -> str:
        """
        @return: Symbol name: string
        """
        if self.valid_stock and self.stock_json:
            return self.stock_json['symbol']
        return ''

    def get_stock_price(self) -> float | None:
        """
        @return: Latest stock price: float
        """
        if self.valid_stock:
            return self.stock_json['latestPrice']
        else:
            return None
