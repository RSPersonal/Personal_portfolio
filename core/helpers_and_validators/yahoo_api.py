import os
import requests
from decouple import config

YAHOO_API_URL = "https://yfapi.net/v6/finance/quote"
YAHOO_API_HEADERS = {
    'x-api-key': os.getenv("YAHOO_FINANCE_API", config("YAHOO_FINANCE_API"))
}


def test_yahoo_api_connection():
    """
    This only test if the connection is successfully, it does not check for correct data.
    @return: Boolean True or False
    """
    query_string = {"symbol": "AAPL"}
    try:
        test_response_for_connection = requests.request("GET", YAHOO_API_URL, headers=YAHOO_API_HEADERS,
                                                        params=query_string)
        return True
    except ConnectionError as error:
        print('Connection error', test_response_for_connection, error)
        return False
    except KeyError as error:
        print('KeyError', test_response_for_connection, error)
        return False


def test_yahoo_api_limit_exceeded():
    """
        This only test if api call limit is exceeded
        @return: Boolean True or False
        """
    query_string = {"symbol": "AAPL"}
    active_connection = test_yahoo_api_connection()

    if active_connection:
        test_response_for_connection = requests.request("GET", YAHOO_API_URL, headers=YAHOO_API_HEADERS,
                                                        params=query_string)
        test_response_for_connection_json = test_response_for_connection.json()
        if 'message' in test_response_for_connection_json and test_response_for_connection_json['message'] == 'Limit Exceeded':
            return True
        else:
            return False


def get_stock_data(user_input_symbol: str):
    """
    Get single stock data object
    @param user_input_symbol: str
    @return: Stock data object (json format)
    """
    query_string = {"symbols": f"{user_input_symbol}"}
    response_from_api_call = requests.request("GET", YAHOO_API_URL, headers=YAHOO_API_HEADERS, params=query_string)
    stock_data_object = response_from_api_call.json()
    return stock_data_object
