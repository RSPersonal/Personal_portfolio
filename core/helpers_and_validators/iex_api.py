import requests
import os
from decouple import config

BASE_URL = 'https://cloud.iexapis.com/v1/'
API_KEY = os.getenv("IEXCLOUD_API_KEY", config("IEXCLOUD_API_KEY"))


def get_stock_package(user_input_stock_symbol):
    response = requests.get(
        f'https://cloud.iexapis.com/stable/stock/{user_input_stock_symbol}/quote?token={API_KEY}').json()


if __name__ == '__main__':
    get_stock_price()
