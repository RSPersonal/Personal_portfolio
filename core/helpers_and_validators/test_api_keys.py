import unittest
import os
import requests
import sentry_sdk
from decouple import config

URL = "https://yfapi.net/v6/finance/quote"

QUERYSTRING = {"symbols": "AAPL"}

HEADERS = {
    'x-api-key': os.getenv("YAHOO_FINANCE_API", config("YAHOO_FINANCE_API"))
}

try:
    response = requests.request("GET", URL, headers=HEADERS, params=QUERYSTRING)
    RESPONSE_API_CALL_YAHOO_API = response.json()
except KeyError as error:
    sentry_sdk.capture_exception(error)
    RESPONSE_API_CALL_YAHOO_API = {}

LIMIT_EXCEEDED = False
if RESPONSE_API_CALL_YAHOO_API and RESPONSE_API_CALL_YAHOO_API['message'] == 'Limit Exceeded':
    LIMIT_EXCEEDED = True


class TestApiKeys(unittest.TestCase):
    """
    Test api keys from yahoo
    """

    def test_yahoo_connection(self):
        """
        @return: None
        """
        if LIMIT_EXCEEDED is False:
            self.assertEqual(RESPONSE_API_CALL_YAHOO_API["quoteResponse"]["result"][0]["symbol"], 'AAPL')
        else:
            print('!YAHOO API CALLS EXCEEDED!')
            self.assertEqual(LIMIT_EXCEEDED, True)


if __name__ == '__main__':
    unittest.main()
