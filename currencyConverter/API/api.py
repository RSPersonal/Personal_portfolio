#The API class for converting the currency

#Dependencies
import json
import requests
from requests import exceptions

#API KEY
API_KEY = "7666b7a2889d6bd686dc"

class Converter():
    """Main class for converting methods"""
    def convert_currency(from_currency, to_currency):
        query = from_currency.upper() + "_" + to_currency.upper() + ","  + to_currency + "_" + from_currency
        url = f"https://free.currconv.com/api/v7/convert?q={query}&compact=ultra&apiKey={API_KEY}"
        try:
            response = requests.get(url)
            json_data = response.json()
            print(json_data)
        except requests.exceptions.exceptions.RequestException as e:
            raise (e)
            
       
test = Converter.convert_currency("USD", "EUR")