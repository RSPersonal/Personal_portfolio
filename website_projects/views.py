import sentry_sdk
from django.shortcuts import render
from .models import PropertyModel
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404


def projects_overview(request):
    return render(request, 'website-projects/website_overview.html')


def real_estate_example(request):
    context = {}
    properties = PropertyModel.objects.order_by('added_on')
    context['properties'] = properties
    return render(request, 'website-projects/real-estate-agent/real_estate_agent_homepage.html', context=context)


def property_detail(request, property_id):
    context = {}
    property_data = get_object_or_404(PropertyModel, id=property_id)
    return render(request, 'website-projects/real-estate-agent/property_detail.html', context=context)
