import os

import requests
import sentry_sdk
from django.shortcuts import render
from .models import PropertyModel
from django.shortcuts import get_object_or_404
from django.db.models import Max
from decouple import config
from core.helpers_and_validators.extraction_helper import extract_postal_code
from core.helpers_and_validators.valuation_service import get_properties_within_postal_code_range_and_nla_range, \
    get_mean_property_price
from website_projects import services


def projects_overview(request):
    return render(request, 'website-projects/website_overview.html')  # pragma no cover


def real_estate_homepage(request):
    context = {}
    properties = PropertyModel.objects.order_by('added_on')[:3]
    context['properties'] = properties
    return render(request, 'website-projects/real-estate-agent/real_estate_agent_homepage.html',
                  context=context)  # pragma no cover


def property_detail(request, property_id):
    context = {}
    property_data = get_object_or_404(PropertyModel, pk=property_id)
    context['property'] = property_data
    return render(request, 'website-projects/real-estate-agent/property_detail.html',
                  context=context)  # pragma no cover


def sale_properties(request):
    context = {}
    active_cities = services.get_all_active_cities(PropertyModel)

    active_property_types = PropertyModel.objects.all().values_list('building_type', flat=True).distinct()
    active_sale_properties = PropertyModel.objects.filter(type_of_property='Koop').order_by('added_on')

    # response = requests.request("GET", "http://127.0.0.1:8000/api/v1/properties/sale/Zwolle").json()

    if request.method == 'POST' and 'filterSubmitButton' in request.POST:
        user_city_input = request.POST.get('userCityInput')
        from_price_range_input = int(request.POST.get('priceRangeFromInput'))
        to_price_range_input = int(request.POST.get('priceRangeToInput'))
        max_ask_price = PropertyModel.objects.aggregate(Max('ask_price'))

        if user_city_input and from_price_range_input and to_price_range_input:
            query_result = PropertyModel.objects.filter(city=user_city_input).filter(
                ask_price__range=(from_price_range_input, to_price_range_input))
        elif user_city_input and from_price_range_input:
            query_result = PropertyModel.objects.filter(city=user_city_input).filter(
                ask_price__range=(from_price_range_input, max_ask_price['ask_price__max']))
        elif user_city_input:
            query_result = PropertyModel.objects.filter(city=user_city_input)
        else:
            query_result = []

        active_sale_properties = query_result
    context['city_filters'] = active_cities
    context['active_properties'] = active_sale_properties
    context['object_types'] = active_property_types
    return render(request, 'website-projects/real-estate-agent/sale_properties.html', context=context)


def rental_properties(request):
    context = {}
    # Here comes the form
    active_cities = active_cities = services.get_all_active_cities(PropertyModel)
    active_rental_properties = PropertyModel.objects.filter(type_of_property='Huur').order_by('added_on')

    # response = requests.request("GET", "http://127.0.0.1:8000/api/v1/properties/sale/Zwolle").json()
    context['city_filters'] = active_cities
    context['active_properties'] = active_rental_properties
    return render(request, 'website-projects/real-estate-agent/rental_properties.html', context=context)


def real_estate_services(request):
    context = {}

    return render(request, 'website-projects/real-estate-agent/real_estate_services.html', context=context)


def real_estate_valuation(request):
    context = {'google_places_key': os.getenv('GOOGLE_PLACES_API', config('GOOGLE_PLACES_API'))}
    if request.method == 'POST' and 'searchAddressSubmitButton' in request.POST:
        # TODO expand test for input of user
        # TODO test should contain following cases: no input, mean price calculation
        user_input_nla = int(request.POST.get('nla'))
        user_input_city = request.POST.get('locality')
        user_input_type_of_object = request.POST.get('typeOfObject')
        clean_postal_code = extract_postal_code(request.POST.get('postcode'))
        user_input_radius = int(request.POST.get('radius'))
        try:
            postal_code_range = requests.get(f"http://postcode.vanvulpen.nl/afstand/{clean_postal_code}/{user_input_radius}/").json()
        except ConnectionError as e:
            sentry_sdk.capture_exception(e)
            postal_code_range = None

        # Makes no sense to search for properties if we have no postal code range
        if postal_code_range:
            queried_properties = get_properties_within_postal_code_range_and_nla_range(postal_code_range,
                                                                                       user_input_type_of_object,
                                                                                       user_input_nla, user_input_city)
            calculated_mean_property_price = get_mean_property_price(queried_properties)

            if len(queried_properties) > 0:
                context['found_objects'] = len(queried_properties)
            else:
                context['no_objects_found'] = True
            if calculated_mean_property_price:
                context['final_calculated_mean_price'] = calculated_mean_property_price
            else:
                context['final_calculated_mean_price'] = 0.0
            context['found_properties'] = queried_properties

        context['user_input_postal_code'] = clean_postal_code
        context['user_input_city'] = user_input_city
    return render(request, 'website-projects/real-estate-agent/real_estate_valuation.html', context=context)


def real_estate_sale_service(request):
    context = {}
    return render(request, 'website-projects/real-estate-agent/real_estate_sale_service.html', context=context)
