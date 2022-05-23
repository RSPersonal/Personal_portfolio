import requests
from django.shortcuts import render
from .models import PropertyModel
from django.shortcuts import get_object_or_404


def projects_overview(request):
    return render(request, 'website-projects/website_overview.html')


def real_estate_homepage(request):
    context = {}
    properties = PropertyModel.objects.order_by('added_on')
    context['properties'] = properties
    return render(request, 'website-projects/real-estate-agent/real_estate_agent_homepage.html', context=context)


def property_detail(request, property_id):
    context = {}
    property_data = get_object_or_404(PropertyModel, id=property_id)
    context['property'] = property_data
    return render(request, 'website-projects/real-estate-agent/property_detail.html', context=context)


def sale_properties(request):
    context = {}
    # Here comes the form

    active_cities = PropertyModel.objects.all().values_list('city', flat=True).distinct()
    active_sale_properties = PropertyModel.objects.filter(type_of_property='SL')

    # response = requests.request("GET", "http://127.0.0.1:8000/api/v1/properties/sale/Zwolle").json()
    context['city_filters'] = active_cities
    context['active_properties'] = active_sale_properties
    return render(request, 'website-projects/real-estate-agent/sale_properties.html', context=context)
