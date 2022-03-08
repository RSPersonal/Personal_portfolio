import os

import requests
from json.decoder import JSONDecodeError
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib import messages
from requests import Response
from decouple import config
from backend.helperclass import InputHelper


# Create your views here.
def api_overview(request):
    return render(request, 'api-examples/api-examples.html')


def geo_api_get_ip(request):
    context = {}

    if request.method == "POST":
        user_ip_input = request.POST.get('ip-address')
        if InputHelper.value(user_ip_input):
            try:
                response: Response = requests.get(
                    f'http://api.ipstack.com/{user_ip_input}?access_key=9e190f3484c23275bc0cb044948ac119')
            except JSONDecodeError as e:
                print(e)
            geo_data = response.json()
            if 'ip' in geo_data:
                context = {
                    'ip': geo_data['ip'],
                    'country_name': geo_data['country_name'],
                    'region_name': geo_data['region_name'],
                    'city': geo_data['city'],
                    'latitude': geo_data['latitude'],
                    'longitude': geo_data['longitude']
                }
            else:
                return JsonResponse(geo_data)
        else:
            messages.add_message(request, messages.INFO, "Input field is empty, please enter you ip!")
    else:
        context = {}
    return render(request, "api-examples/geo-api.html", context)


def currency_converter_call(request):
    context = {}

    if request.method == 'POST':
        from_currency_input = request.POST.get('to-currency')
        amount = request.POST.get('amount')
        if InputHelper.value(from_currency_input) and InputHelper.value(amount):
            api_key = os.getenv('CURRENCY_FREAKS_API_KEY', config('CURRENCY_FREAKS_API_KEY'))
            try:
                response: Response = requests.get(
                    f'https://api.currencyfreaks.com/latest?apikey={api_key}&symbols={from_currency_input}')
            except JSONDecodeError as e:
                print(e)
            requested_currency_data = response.json()
            if 'success' in requested_currency_data:
                messages.add_message(request, messages.INFO, requested_currency_data['error']['message'])
            else:
                converted_amount_in_new_currency = round(
                    float(amount) * float(requested_currency_data['rates'][from_currency_input]), 2)
                context = {
                    'from_currency': from_currency_input,
                    'converted_amount': converted_amount_in_new_currency
                }
        else:
            messages.add_message(request, messages.INFO, 'Wrong input parameters, check input')
    else:
        pass
    return render(request, 'api-examples/currency_converter.html', context=context)
