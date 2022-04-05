import os
import requests
import unittest
from decouple import config

url = "https://yfapi.net/v6/finance/quote"

querystring = {"symbols": "AAPL"}

headers = {
    'x-api-key': os.getenv("YAHOO_FINANCE_API", config("YAHOO_FINANCE_API"))
}

response = requests.request("GET", url, headers=headers, params=querystring)
RESPONSE_API_CALL_YAHOO_API = response.json()


class TestApiKeys(unittest.TestCase):

    def test_yahoo_connection(self):
        self.assertEqual(RESPONSE_API_CALL_YAHOO_API["quoteResponse"]["result"][0]["symbol"], 'AAPL')


if __name__ == '__main__':
    unittest.main()
