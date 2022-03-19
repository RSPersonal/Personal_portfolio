import os
import requests
from django.contrib import messages
from decouple import config
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Portfolio, Positions
from .forms import PortfolioForm, PositionForm
from backend.helper_class import CalculateHelper


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
        for position in positions:
            # Get current market price for profit calculation
            get_stock_json = requests.get(
                f"https://api.polygon.io/v2/aggs/ticker/{position.ticker_name}/prev?adjusted=true&apiKey={os.getenv('POLYGON_API_KEY', config('POLYGON_API_KEY'))}")
            result_api_call = get_stock_json.json()
            # TODO ERROR when newly added position, look nto this
            if result_api_call['resultsCount'] > 0:
                position.current_market_price = result_api_call['results'][0]['c']
                current_market_price_from_api_call = result_api_call['results'][0]['c']
            else:
                current_market_price_from_api_call = 0

            # Total amount invested calculation
            calculated_total_invested = CalculateHelper.calculate_total_amount_invested(position.buy_price,
                                                                                        position.quantity)
            position.amount_invested = calculated_total_invested

            # Profit calculation
            calculated_profit = CalculateHelper.calculate_stock_profit(position.buy_price,
                                                                       current_market_price_from_api_call, position.quantity)
            position.position_profit = round(calculated_profit, 2)

            # Profit in percentage calculation
            calculated_profit_perc = CalculateHelper.calculate_profit_in_percentage(position.buy_price,
                                                                                    position.quantity,
                                                                                    calculated_profit)
            position.position_profit_in_percentage = calculated_profit_perc

        context['positions'] = positions
    else:
        context['active_positions'] = False

    # Adding new positions to database
    if request.method == 'POST':
        form = PositionForm(request.POST)
        if form.is_valid():
            # Getting all the cleaned data for the database entry
            user_input_stock_name = form.cleaned_data['ticker_name']
            user_input_buy_price = form.cleaned_data['buy_price']
            user_input_quantity = form.cleaned_data['quantity']
            user_input_market = form.cleaned_data['market']

            # TODO Write checks for responses and empty data
            get_stock_json = requests.get(
                f"https://api.polygon.io/v2/aggs/ticker/{user_input_stock_name}/prev?adjusted=true&apiKey={os.getenv('POLYGON_API_KEY', config('POLYGON_API_KEY'))}")
            ticker_data = get_stock_json.json()

            # Checking if results came back, otherwise give user notification for bad request
            if ticker_data['resultsCount'] > 0:
                # Adding new entry to Database
                new_stock_entry = Positions(portfolio=portfolio, ticker_name=user_input_stock_name,
                                            buy_price=user_input_buy_price,
                                            current_market_price=ticker_data['results'][0]['c'],
                                            quantity=user_input_quantity, market=user_input_market)
                # Saving the entry to database
                new_stock_entry.save()

                return redirect('portfolio_detail', pk)
            else:
                messages.add_message(request, messages.INFO, "Could not find Stock, make sure you spelled it correct")

    if request.method == 'POST' and 'delete_button' in request.POST:
        if Positions.objects.filter(portfolio=pk).exists():
            Portfolio.objects.filter(portfolio=pk).delete()
        return redirect('stocktracker')

    return render(request, 'database-projects/portfolio_detail.html', context=context)
