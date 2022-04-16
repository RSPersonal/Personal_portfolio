import os
import requests
import unittest
import sentry_sdk
from decouple import config

url = "https://yfapi.net/v6/finance/quote"

querystring = {"symbols": "AAPL"}

headers = {
    'x-api-key': os.getenv("YAHOO_FINANCE_API", config("YAHOO_FINANCE_API"))
}

try:
    response = requests.request("GET", url, headers=headers, params=querystring)
    RESPONSE_API_CALL_YAHOO_API = response.json()
except KeyError as error:
    sentry_sdk.capture_exception(error)
    RESPONSE_API_CALL_YAHOO_API = {}

limit_exceeded = False
if RESPONSE_API_CALL_YAHOO_API and RESPONSE_API_CALL_YAHOO_API['message'] == 'Limit Exceeded':
    limit_exceeded = True


class TestApiKeys(unittest.TestCase):

    def test_yahoo_connection(self):
        if limit_exceeded is False:
            self.assertEqual(RESPONSE_API_CALL_YAHOO_API["quoteResponse"]["result"][0]["symbol"], 'AAPL')
        else:
            print('!YAHOO API CALLS EXCEEDED!')
            self.assertEqual(limit_exceeded, True)


if __name__ == '__main__':
    unittest.main()
