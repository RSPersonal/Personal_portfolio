import os
import requests
from django.contrib import messages
from decouple import config
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Portfolio, Positions
from .forms import PortfolioForm, PositionForm
from core.helper_class import calculations_helper, input_validator_helper

YAHOO_API_URL = "https://yfapi.net/v6/finance/quote"

querystring = {"symbols": "ASHK"}

YAHOO_API_HEADERS = {
    'x-api-key': os.getenv("YAHOO_FINANCE_API", config("YAHOO_FINANCE_API"))
}


# Create your views here
def database_homepage(request):
    context = {}
    return render(request, 'database-projects/database-projects.html', context=context)


@login_required
def stock_tracker_landing_page(request):
    # Getting all portfolio's from user
    portfolio_or_portfolios = Portfolio.objects.filter(user_id=request.user.id)
    # Getting the position data from portfolio
    labels = []
    data = []
    context = {}
    for portfolio in portfolio_or_portfolios:
        get_portfolio_id = portfolio.id
        positions_in_portfolio = Positions.objects.filter(portfolio_id=get_portfolio_id)
        for position in positions_in_portfolio:
            labels.append(position.ticker_name)
            data.append(position.quantity)

        context[f"labels_{get_portfolio_id}"] = labels
        context[f"data_{get_portfolio_id}"] = data
    print(context)
    portfolio_form = PortfolioForm()
    context['portfolios'] = portfolio_or_portfolios
    context['portfolio_form'] = portfolio_form

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

        # Standard variables for total calculation of portfolio
        current_market_price_from_api_call = 0
        calculated_total_amount_invested_in_portfolio = 0
        calculated_total_profit_portfolio = 0
        calculated_total_profit_percentage = 0.0
        calculated_total_positions = 0

        # Check if connection is accessible
        active_connection = True
        try:
            requested_ticker_query_string = {"symbols": "AAPL"}
            response = requests.request("GET", YAHOO_API_URL, headers=YAHOO_API_HEADERS,
                                        params=requested_ticker_query_string)
        except ConnectionError as e:
            print('\nError =', e)
            active_connection = False

        if active_connection:
            for position in positions:
                # Get current market price for profit calculation
                requested_ticker_query_string = {"symbols": f"{position.ticker_name}"}
                get_stock_data = requests.request("GET", YAHOO_API_URL, headers=YAHOO_API_HEADERS,
                                                  params=requested_ticker_query_string)
                result_api_call_json = get_stock_data.json()

                if len(result_api_call_json) != 0 and input_validator_helper.no_value(
                        result_api_call_json["quoteResponse"]["result"]):
                    messages.add_message(request, messages.INFO, result_api_call_json["quoteResponse"]["error"])
                    break
                elif len(result_api_call_json) != 0 and input_validator_helper.value(
                        result_api_call_json["quoteResponse"]["result"]):
                    position.current_market_price = result_api_call_json["quoteResponse"]["result"][0][
                        "regularMarketPrice"]
                    current_market_price_from_api_call = result_api_call_json["quoteResponse"]["result"][0][
                        "regularMarketPrice"]

                # Total amount invested calculation
                calculated_total_invested = calculations_helper.calculate_total_amount_invested(position.buy_price,
                                                                                                position.quantity)
                position.amount_invested = calculated_total_invested
                calculated_total_amount_invested_in_portfolio += calculated_total_invested

                # Profit calculation
                calculated_profit = calculations_helper.calculate_stock_profit(position.buy_price,
                                                                               current_market_price_from_api_call,
                                                                               position.quantity)
                position.position_profit = round(calculated_profit, 2)
                calculated_total_profit_portfolio += calculated_profit

                # Profit in percentage calculation
                calculated_profit_perc = calculations_helper.calculate_profit_in_percentage(position.buy_price,
                                                                                            position.quantity,
                                                                                            calculated_profit)
                calculated_total_profit_percentage += calculated_profit_perc
                position.position_profit_in_percentage = calculated_profit_perc

                # Total positions
                calculated_total_positions += 1

            # Save it to the portfolio object to show later in portfolio overview
            portfolio.total_positions = calculated_total_positions
            portfolio.total_amount_invested = calculated_total_amount_invested_in_portfolio
            portfolio.total_profit = round(calculated_total_profit_portfolio, 2)
            portfolio.total_profit_percentage = calculations_helper.calculate_portfolio_profit_in_percentage(
                calculated_total_amount_invested_in_portfolio, calculated_total_profit_portfolio)
            portfolio.save()
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

            requested_ticker_query_string = {"symbols": f"{user_input_stock_name}"}
            get_stock_data = requests.request("GET", YAHOO_API_URL, headers=YAHOO_API_HEADERS,
                                              params=requested_ticker_query_string)
            result_stock_data_json = get_stock_data.json()

            # Checking if results came back, otherwise give user notification for bad request
            if input_validator_helper.value(result_stock_data_json["quoteResponse"]["result"]) and \
                    result_stock_data_json["quoteResponse"]["result"][0]["symbol"] == user_input_stock_name:
                # Adding new entry to Database
                new_stock_entry = Positions(portfolio=portfolio, ticker_name=user_input_stock_name,
                                            buy_price=user_input_buy_price,
                                            current_market_price=result_stock_data_json["quoteResponse"]["result"][0][
                                                "regularMarketPrice"],
                                            quantity=user_input_quantity, market=user_input_market)
                # Saving the entry to database
                new_stock_entry.save()

                return redirect('portfolio_detail', pk)
            else:
                messages.add_message(request, messages.INFO, "Could not find Stock, make sure you spelled it correct")

    # Delete position
    if request.method == 'POST' and 'delete_position_button' in request.POST:
        Positions.objects.get(id=request.POST.get('id')).delete()
        return redirect('portfolio_detail', pk)

    # Delete portfolio
    if request.method == 'POST' and 'delete_button' in request.POST:
        if Positions.objects.filter(portfolio=pk).exists() or Portfolio.objects.get(id=pk):
            Portfolio.objects.get(id=pk).delete()
            return redirect('stocktracker')

    return render(request, 'database-projects/portfolio_detail.html', context=context)
