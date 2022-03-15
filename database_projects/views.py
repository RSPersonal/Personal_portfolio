from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Portfolio, Positions
from .forms import PortfolioForm, PositionForm


# Create your views here
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
    portfolio = Portfolio.objects.get(id=pk)
    position_form = PositionForm()

    context = {
        'position_form': position_form,
        'portfolio': portfolio
    }
    # See if there are any active positions
    if Positions.objects.filter(portfolio=pk).exists():
        positions = Positions.objects.filter(portfolio=pk).order_by('added_on')
        print(positions)
        context['positions'] = positions
    else:
        context['active_positions'] = False

    # Adding new positions to database
    if request.method == 'POST':
        form = PositionForm(request.POST)
        if form.is_valid():
            user_input_stock_name = form.cleaned_data['ticker_name']
            user_input_buy_price = form.cleaned_data['buy_price']
            user_input_quantity = form.cleaned_data['quantity']
            user_input_market = form.cleaned_data['market']

            new_stock_entry = Positions(portfolio=portfolio, ticker_name=user_input_stock_name,
                                        buy_price=user_input_buy_price,
                                        quantity=user_input_quantity, market=user_input_market)
            new_stock_entry.save()
            return redirect('portfolio_detail', pk)

    if request.method == 'POST' and 'delete_button' in request.POST:
        if Positions.objects.filter(portfolio=pk).exists():
            Portfolio.objects.filter(portfolio=pk).delete()
        return redirect('stocktracker')

    return render(request, 'database-projects/portfolio_detail.html', context=context)
