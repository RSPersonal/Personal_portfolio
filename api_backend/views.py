import requests
from json.decoder import JSONDecodeError
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib import messages
from requests import Response

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
        from_currency_input = request.POST.get('')
        to_currency_input = request.POST.get('')
        amount = float(request.POST.get(''))
        if InputHelper.value(from_currency_input) and InputHelper.value(amount) and InputHelper.value(
                to_currency_input):
            try:
                response: Response = request.get(
                    f'https://api.currencyfreaks.com/latest?apikey=0421374edc404ab7a49caf0433642541&symbols={to_currency_input}')
            except JSONDecodeError as e:
                print(e)
            requested_currency_data = response.json()
            converted_amount_in_new_currency = amount * float(requested_currency_data['rates'])
            context = {
                'from_currency': from_currency_input,
                'to_currency': to_currency_input,
                'converted_amount': converted_amount_in_new_currency
            }
        else:
            messages.add_message(request, messages.INFO, 'Wrong input parameters, check input')
    else:
        context = {}
    return render(request, 'api-examples/currency_converter.html', context=context)
