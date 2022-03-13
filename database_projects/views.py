from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Portfolio, Positions
from .forms import PortfolioForm, PositionForm


# Create your views heree
def database_homepage(request):
    context = {}
    return render(request, 'database-projects/database-projects.html', context=context)


@login_required
def stock_tracker_landing_page(request):
    portfolio_or_portfolios = Portfolio.objects.all()
    portfolio_form = PortfolioForm()
    context = {
        'portfolios': portfolio_or_portfolios,
        'portfolio_form': portfolio_form
    }

    if request.method == 'POST':
        form = PortfolioForm(request.POST)
        if form.is_valid():
            cleaned_user_portfolio_name = form.cleaned_data['portfolio_name']
            new_portfolio_entry = Portfolio(portfolio_name=cleaned_user_portfolio_name, user_id=request.user.id)
            new_portfolio_entry.save()
    return render(request, 'database-projects/stocktracker.html', context=context)


@login_required
def portfolio_detail(request, pk):
    portfolio_name = Portfolio.objects.get(id=pk)
    position_form = PositionForm()

    context = {
        'position_form': position_form,
        'portfolio_name': portfolio_name
    }
    if Positions.objects.filter(pk=pk).exists():
        positions = Positions.objects.get(portfolio_id=pk)
        context['position'] = positions
    else:
        context['active_positions'] = False

    if request.method == 'POST':
        pass
    return render(request, 'database-projects/portfolio_detail.html', context=context)
