from django.shortcuts import render


def projects_overview(request):
    return render(request, 'website-projects/website_overview.html')


def real_estate_example(request):
    return render(request, 'website-projects/real-estate-agent/real_estate_agent_homepage.html')
