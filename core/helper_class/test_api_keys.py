import os

import requests

url = "https://yfapi.net/v6/finance/quote"

querystring = {"symbols": "AAPL"}

headers = {
    'x-api-key': os.getenv("YAHOO_FINANCE_API", config("YAHOO_FINANCE_API"))
}

response = requests.request("GET", url, headers=headers, params=querystring)
response_json = response.json()
print(response_json["quoteResponse"])
