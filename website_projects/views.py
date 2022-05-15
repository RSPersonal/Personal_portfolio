from django.shortcuts import render
from .models import PropertyModel

def projects_overview(request):
    return render(request, 'website-projects/website_overview.html')


def real_estate_example(request):
    context = {}
    properties = PropertyModel.objects.order_by('added_on')
    context['properties'] = properties
    return render(request, 'website-projects/real-estate-agent/real_estate_agent_homepage.html', context=context)
