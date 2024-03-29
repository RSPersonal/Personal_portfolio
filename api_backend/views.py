import os
import requests
from json.decoder import JSONDecodeError
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.contrib import messages
from decouple import config
from .forms import CurrencyForm
from core.helpers_and_validators import input_validator
from rest_framework.decorators import api_view
from rest_framework.response import Response
from database_projects.models import Portfolio
from website_projects.models import PropertyModel
from .serializers import PortfolioSerializer, PropertySerializer
from core.core_scripts import keyword_finder_core


# Create your views here.
def api_overview(request):
    return render(request, 'api-examples/api-examples.html')


def geo_api_get_ip(request):
    context = {}

    if request.method == "POST":
        user_ip_input = request.POST.get('ip-address')
        if input_validator.value(user_ip_input):
            try:
                response = requests.get(
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
                context['success'] = False
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
        if input_validator.value(from_currency_input) and form.is_valid():
            amount = form.cleaned_data['amount']
            api_key = os.getenv('CURRENCY_FREAKS_API_KEY', config('CURRENCY_FREAKS_API_KEY'))
            requested_currency_data = {}
            try:
                response = requests.get(
                    f'https://api.currencyfreaks.com/latest?apikey={api_key}&symbols={from_currency_input}')
                requested_currency_data = response.json()
            except JSONDecodeError as e:
                print(e)
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


@api_view(['GET'])
def endpoint_chart_data(request):
    return Response({'message': 'success', 'endpoint': 'chart data from user portfolio'})


@api_view(['GET'])
def get_portfolio_monthly_profit(request, pk):
    """
    @param request:
    @param pk: int portfolio id to get monthly profit data
    @return: user_id and array with the monthly profits for requested portfolio
    """
    if request.method == 'GET':
        user_input_id = int(pk)
        if Portfolio.objects.filter(pk=user_input_id).exists():
            portfolio = Portfolio.objects.get(pk=user_input_id)
            serializer = PortfolioSerializer(portfolio)
            return Response({'message': 'success',
                             'data': serializer.data})
        else:
            return Response({'message': 'failed',
                             'data': []})
    return Response({'message': 'success', 'data': []})


@api_view(['GET'])
def get_user_desired_properties(request, user_input_city):
    """
    @param request:
    @param user_input_city:
    @return:
    """
    if request.method == 'GET':
        # TODO JUST FOR TESTING
        if PropertyModel.objects.filter(city=user_input_city).exists() or PropertyModel.objects.filter(city__icontains=user_input_city).exists():
            data = {'message': 'success',
                    'status': 200,
                    'data': {
                        'properties': {}
                        }
                    }

            properties_in_city = PropertyModel.objects.filter(city=user_input_city)
            print(data['data'], properties_in_city)
            for count, query_property in enumerate(properties_in_city):
                serializer = PropertySerializer(query_property)
                print(data['data'])
                data['data']['properties'][count] = serializer.data
            return Response(data)
        else:
            return Response({'message': 'success',
                             'status': 404,
                             'data': f'No properties found for {user_input_city}'})
    return Response({'message': 'success', 'data': []})


def keyword_finder(request):
    """
    @param request:
    @return:
    """
    # TODO build unittest for this functionality
    context = {}
    if request.method == 'POST' and 'user_file' in request.FILES:
        # We want to decode it for the regex
        # TODO Build check to validate uploaded file is only .txt file extension
        uploaded_file = request.FILES['user_file']
        file_text = uploaded_file.read().decode('utf8')
        uploaded_file.close()

        # Get desired output and clean the input
        user_desired_output = request.POST.get('txt_file_or_output').lower().replace(' ', '')
        user_input_keyword = request.POST.get('keyword').lower().strip()
        if user_input_keyword == '':
            messages.add_message(request, messages.INFO, 'No keyword entered.')
        else:
            # Start the search and return desired output
            found_keywords = keyword_finder_core.find_keywords_in_text_file(user_input_keyword, user_desired_output, file_text)
            if user_desired_output == 'outputinbrowser':
                context['amount_keys_found'] = found_keywords['keys_found']
                context['found_keywords'] = found_keywords['data']
            elif user_desired_output == 'json':
                return JsonResponse(found_keywords)
            else:
                response = HttpResponse(found_keywords,
                                        content_type='text/plain',
                                        headers={'Content-Disposition': 'attachment; filename="found_keywords.txt"'},
                                        )
                return response
    else:
        context['no_file'] = True
    return render(request, 'api-examples/keyword_finder.html', context=context)
