import requests
import os
from decouple import config

BASE_URL = 'http://api.marketstack.com/v1/intraday/latest?access_key='
ACCESS_KEY = os.getenv("MARKETSTACK_API_KEY", config("MARKETSTACK_API_KEY"))


def test_api_connection():
    """
    Test api connection
    @return: boolean true or false
    """
    response = requests.get(f"{BASE_URL}{ACCESS_KEY}&symbols=AAPL").json()
    if response['data']:
        return True
    else:
        return False


def get_stock_price(user_input_stock_ticker: str):
    """
    @param user_input_stock_ticker:  str
    @return: current stock price for ticker symbol
    """
    try:
        response = requests.get(f"{BASE_URL}{ACCESS_KEY}&symbols={user_input_stock_ticker}").json()
        return response['data'][0]['open']
    except ConnectionError as e:
        return {'connection': 'failed',
                'error': e}
    except IndexError as e:
        return {'connection': 'success',
                'error': e}


def get_stock_ticker_symbol(user_input_stock_ticker: str):
    """
    @param user_input_stock_ticker: string
    @return: string: Ticker name
    """
    try:
        response = requests.get(f"{BASE_URL}{ACCESS_KEY}&symbols={user_input_stock_ticker}").json()
        return response['data'][0]['symbol']
    except ConnectionError as e:
        return {'connection': 'failed',
                'error': e}
    except IndexError as e:
        return {'connection': 'success',
                'error': e}
