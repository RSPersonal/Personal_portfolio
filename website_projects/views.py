from django.shortcuts import render


def projects_overview(request):
    return render(request, 'website-projects/website_overview.html')


def real_estate_example(request):
    return render(request, 'website-projects/real_estate_example.html')
