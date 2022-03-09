from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Portfolio


# Create your views here.


def database_homepage(request):
    context = {}
    return render(request, 'database-projects/database-projects.html', context=context)


@login_required
def stock_tracker_landing_page(request):
    portfolio_or_portfolios = Portfolio.objects.all()
    context = {
        'portfolios': portfolio_or_portfolios
    }
    return render(request, 'database-projects/stocktracker.html', context=context)


@login_required
def portfolio_detail(request, pk):
    portfolio = Portfolio.objects.get(pk=pk)

    context = {
        'portfolio': portfolio
    }
    return render(request, 'database-projects/portfolio_detail.html', context=context)
