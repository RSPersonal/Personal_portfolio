import requests
import os
from decouple import config
import sentry_sdk

BASE_URL = 'http://api.marketstack.com/v1/intraday/latest?access_key='
ACCESS_KEY = os.getenv("MARKETSTACK_API_KEY", config("MARKETSTACK_API_KEY"))


def test_api_connection():
    """
    Test api connection
    @return: boolean true or false
    """
    try:
        response = requests.get(f"{BASE_URL}{ACCESS_KEY}&symbols=AAPL").json()
        return True
    except ConnectionError as e:
        sentry_sdk.capture_exception(e)
        return False
    except KeyError as e:
        sentry_sdk.capture_exception(e)
        return False


def check_if_limit_exceeded():
    """
    Check if usage limit is reached
    @return: bool true if reached, false if not
    """
    response = requests.get(f"{BASE_URL}{ACCESS_KEY}&symbols=AAPL").json()
    if response['error']['code'] == 'usage_limit_reached':
        return True
    else:
        return False


def get_stock_price(user_input_stock_ticker: str):
    """
    @param user_input_stock_ticker:  str
    @return: current stock price for ticker symbol
    """
    if test_api_connection() and not check_if_limit_exceeded():
        try:
            response = requests.get(f"{BASE_URL}{ACCESS_KEY}&symbols={user_input_stock_ticker}").json()
            return response['data'][0]['open']
        except ConnectionError as e:
            return {'connection': 'failed',
                    'error': e}
        except IndexError as e:
            return {'connection': 'success',
                    'error': e}
    else:
        return {'connection': 'failed',
                'error': 'connection error or limit is exceeded'}


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
    except KeyError as e:
        return {'connection': 'success',
                'error': e}
