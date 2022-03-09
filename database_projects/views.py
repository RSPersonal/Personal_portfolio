from django.shortcuts import render


# Create your views here.


def database_homepage(request):
    context = {}
    return render(request, 'database-projects/database-projects.html', context=context)


def stock_tracker(request):
    context = {}
    return render(request, 'database-projects/stocktracker.html', context=context)
