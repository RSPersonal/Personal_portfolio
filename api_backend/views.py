import os

import requests
from json.decoder import JSONDecodeError
from django.shortcuts import render
from django.contrib import messages
from requests import Response
from decouple import config
from .forms import CurrencyForm
from core.helpers_and_validators import input_validator
from rest_framework.decorators import api_view
from rest_framework.response import Response
from database_projects.models import Portfolio
from .serializers import PortfolioSerializer


# Create your views here.
def api_overview(request):
    return render(request, 'api-examples/api-examples.html')


def geo_api_get_ip(request):
    context = {}

    if request.method == "POST":
        user_ip_input = request.POST.get('ip-address')
        if input_validator_helper.value(user_ip_input):
            try:
                response: Response = requests.get(
                    f'http://api.ipstack.com/{user_ip_input}?access_key=9e190f3484c23275bc0cb044948ac119')
                geo_data = response.json()
            except JSONDecodeError as e:
                print(e)
                geo_data = {}

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
                context['succes'] = False
        else:
            messages.add_message(request, messages.INFO, "Input field is empty, please enter you ip!")
    else:
        context = {}
    return render(request, "api-examples/geo-api.html", context)


def currency_converter_call(request):
    form = CurrencyForm()
    context = {
        'form': form
    }
    if request.method == 'POST':
        from_currency_input = request.POST.get('to-currency')
        form = CurrencyForm(request.POST)
        if input_validator_helper.value(from_currency_input) and form.is_valid():
            amount = form.cleaned_data['amount']
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
                context['from_currency'] = from_currency_input
                context['converted_amount'] = converted_amount_in_new_currency
        else:
            messages.add_message(request, messages.INFO, 'Wrong input parameters, check input')
    else:
        pass
    return render(request, 'api-examples/currency_converter.html', context=context)


@api_view(['GET', 'POST'])
def hello_world(request, pk):
    if request.method == 'GET':
        user_input_id = int(pk)
        if Portfolio.objects.filter(pk=user_input_id).exists():
            data = 'Found portfolio'
            portfolio = Portfolio.objects.get(pk=user_input_id)
            serializer = PortfolioSerializer(portfolio)
            return Response({'message': 'succes',
                             'data': serializer.data})
        else:
            data = 'Did not find requested portfolio'
            return Response({'message': 'failed',
                             'data': []})
    return Response({'message': 'Hello World'})
