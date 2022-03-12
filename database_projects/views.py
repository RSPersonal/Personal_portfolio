from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Portfolio, Positions


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
    context = {}
    if Portfolio.objects.filter('user_id').get('portfolio_name'):
        context['portfolio_name'] = Portfolio.objects.filter('user_id').get('portfolio_name')
    else:
        context['portfolio_name'] = False

    if Positions.objects.get(portfolio_id=pk):
        positions = Positions.objects.get(portfolio_id=pk)
        context['position'] = positions
    else:
        context['success'] = False

    return render(request, 'database-projects/portfolio_detail.html', context=context)
