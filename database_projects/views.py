import os
import csv
from datetime import date
import sentry_sdk
from django.contrib import messages
from decouple import config
from django.http import FileResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Portfolio, Positions
from .forms import PortfolioForm, PositionForm
from core.helpers_and_validators import calculator, input_validator, yahoo_api
from core.core_pdf_generator import core_pdf_generator
from datetime import datetime

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
    current_user_id = request.user.id
    portfolio_or_portfolios = Portfolio.objects.filter(user_id=current_user_id)
    # Getting the position data from portfolio
    context = {}
    portfolio_form = PortfolioForm()

    context['portfolios'] = portfolio_or_portfolios
    context['portfolio_form'] = portfolio_form
    context['labels_monthly'] = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']

    #  Adding the total profit to correct month.
    current_month = datetime.now()
    current_month_for_data_array = (current_month.month - 1)
    for portfolio in portfolio_or_portfolios:
        try:
            new_monthly_profit = portfolio.monthly_profit[current_month_for_data_array] = portfolio.total_profit
            portfolio.save()
        except KeyError as error:
            sentry_sdk.capture_exception(error)
        except IndexError as error:
            sentry_sdk.capture_exception(error)
            new_monthly_profit = portfolio.monthly_profit.append(0)
            portfolio.save()

        # Reset the portfolio figures if no active positions
        if portfolio.total_positions == 0:
            portfolio.total_amount_invested = 0
            portfolio.total_profit = 0
            portfolio.total_profit_percentage = 0.0
            portfolio.data_for_chart_array = []
            portfolio.labels_array = []
            portfolio.total_positions = 0
            portfolio.save()

        # Get the monthly profits for visualisation
        # try:
        #     response = requests.request('GET', f"http://127.0.0.1:8000/api/v1/chart-data/{portfolio.id}",
        #                                 timeout=5).json()
        #     portfolio_monthly_profits = response['data']['monthly_profit']
        # except ConnectionError as error:
        #     sentry_sdk.capture_exception(error)
        #     portfolio_monthly_profits = []
        #
        # context[f"monthly_profit_{portfolio.id}"] = portfolio_monthly_profits

    # Adding new portfolio
    if request.method == 'POST':
        form = PortfolioForm(request.POST)
        if form.is_valid():
            monthly_profit_array_until_current_month = []
            for i in range(0, current_month.month):
                monthly_profit_array_until_current_month.append(0)

            print(monthly_profit_array_until_current_month)
            cleaned_user_portfolio_name = form.cleaned_data['portfolio_name']
            new_portfolio_entry = Portfolio(portfolio_name=cleaned_user_portfolio_name,
                                            user_id=request.user.id,
                                            data_for_chart_array=[],
                                            labels_array=[],
                                            monthly_profit=monthly_profit_array_until_current_month
                                            )
            new_portfolio_entry.save()
    return render(request, 'database-projects/stocktracker.html', context=context)


@login_required
def portfolio_detail(request, pk):
    # General checks for yahoo api calls
    limit_exceeded = yahoo_api.test_yahoo_api_limit_exceeded()
    active_connection = yahoo_api.test_yahoo_api_connection()

    portfolio = Portfolio.objects.get(id=pk)
    position_form = PositionForm()

    context = {
        'position_form': position_form,
        'portfolio': portfolio
    }

    # Lookup if there are any active positions
    if Positions.objects.filter(portfolio=pk).exists():
        # Get all positions
        positions = Positions.objects.filter(portfolio=pk).order_by('added_on')

        # Standard variables for total calculation of portfolio
        current_market_price_from_api_call = 0
        calculated_total_amount_invested_in_portfolio = 0
        calculated_total_profit_portfolio = 0
        calculated_total_profit_percentage = 0.0
        calculated_total_positions = 0
        labels_for_portfolio_chart = []
        data_for_portfolio_chart = []

        if not active_connection or limit_exceeded:
            if yahoo_api.test_yahoo_api_limit_exceeded():
                limit_exceeded = True
                messages.add_message(request, messages.INFO,
                                     'API call limit exceeded. Profit calculation is not correct due to market price is set to 0 in case of api call limit is exceeded.')
            elif not active_connection:
                messages.add_message(request, messages.INFO, 'No active connection, check if API key is valid.')

        if active_connection:
            for position in positions:
                key_error = False

                # Get stock data
                try:
                    requested_stock_data_json = yahoo_api.get_stock_data(f"{position.ticker_name}")
                except KeyError as captured_error:
                    sentry_sdk.capture_exception(captured_error)
                    key_error = True

                if limit_exceeded is False and key_error is False:
                    stock_data_object = requested_stock_data_json["quoteResponse"]["result"][0]
                else:
                    stock_data_object = {}

                # Get current market price for profit calculation
                if limit_exceeded is False and key_error is False and input_validator.no_value(
                        requested_stock_data_json["quoteResponse"]["result"]):
                    messages.add_message(request, messages.INFO, requested_stock_data_json["quoteResponse"]["error"])
                    break
                elif input_validator.value(stock_data_object) and limit_exceeded is False and key_error is False:
                    position.current_market_price = stock_data_object["regularMarketPrice"]
                    current_market_price_from_api_call = stock_data_object["regularMarketPrice"]
                else:
                    position.current_market_price = 0
                    current_market_price_from_api_call = 0

                # Total amount invested calculation
                calculated_total_invested = calculator.calculate_total_amount_invested(position.buy_price,
                                                                                       position.quantity)
                position.amount_invested = calculated_total_invested
                calculated_total_amount_invested_in_portfolio += calculated_total_invested

                # Profit calculation
                if position.current_market_price == 0:
                    calculated_profit = 0
                else:
                    calculated_profit = calculator.calculate_stock_profit(position.buy_price,
                                                                          current_market_price_from_api_call,
                                                                          position.quantity)
                position.position_profit = round(calculated_profit, 2)
                calculated_total_profit_portfolio += calculated_profit

                # Profit in percentage calculation
                calculated_profit_perc = calculator.calculate_profit_in_percentage(position.buy_price,
                                                                                   position.quantity,
                                                                                   calculated_profit)
                calculated_total_profit_percentage += calculated_profit_perc
                position.position_profit_in_percentage = calculated_profit_perc

                # Total positions
                calculated_total_positions += 1

                # Labels for Portfolio chart
                if limit_exceeded is False:
                    labels_for_portfolio_chart.append(stock_data_object["symbol"])

                # Data for Portfolio chart
                data_for_portfolio_chart.append(position.quantity)

                # Save some to the position model
                position.amount_invested = round(calculated_total_invested, 2)
                position.position_profit = round(calculated_profit, 2)
                position.position_profit_in_percentage = round(calculated_profit_perc, 2)
                position.save()

            # Save it to the portfolio object to show later in portfolio overview
            portfolio.total_positions = calculated_total_positions
            portfolio.total_amount_invested = calculated_total_amount_invested_in_portfolio
            portfolio.total_profit = round(calculated_total_profit_portfolio, 2)
            portfolio.total_profit_percentage = calculator.calculate_portfolio_profit_in_percentage(
                calculated_total_amount_invested_in_portfolio, calculated_total_profit_portfolio)
            portfolio.labels_array = labels_for_portfolio_chart
            portfolio.data_for_chart_array = data_for_portfolio_chart
            portfolio.save()
            context['positions'] = positions
    else:
        context['active_positions'] = False

    # Adding new positions to database
    if request.method == 'POST' and 'add_position_button' in request.POST:
        add_position_form = PositionForm(request.POST)
        if add_position_form.is_valid():
            # Getting all the cleaned data for the database entry
            user_input_add_form_stock_name = add_position_form.cleaned_data['ticker_name']
            user_input_add_form_buy_price = add_position_form.cleaned_data['buy_price']
            user_input_add_form_quantity = add_position_form.cleaned_data['quantity']
            user_input_add_form_market = add_position_form.cleaned_data['market']
            found_stock = False

            if active_connection and limit_exceeded is False:
                result_stock_data_json = yahoo_api.get_stock_data(f"{user_input_add_form_stock_name}")

                if input_validator.value(result_stock_data_json["quoteResponse"]["result"]) and \
                        result_stock_data_json["quoteResponse"]["result"][0]["symbol"] == user_input_add_form_stock_name:
                    found_stock = True
                    current_market_price_from_api_call_or_zero = result_stock_data_json["quoteResponse"]["result"][0][
                        "regularMarketPrice"]
            else:
                current_market_price_from_api_call_or_zero = 0

            if limit_exceeded:
                messages.add_message(request, messages.INFO, 'API CALL LIMIT EXCEEDED.')
            elif found_stock is False:
                messages.add_message(request, messages.INFO, "Could not find Stock, make sure you spelled it correct")

            # Adding new entry to Database
            new_stock_entry = Positions(portfolio=portfolio, ticker_name=user_input_add_form_stock_name,
                                        buy_price=user_input_add_form_buy_price,
                                        current_market_price=current_market_price_from_api_call_or_zero,
                                        quantity=user_input_add_form_quantity,
                                        market=user_input_add_form_market)
            # Saving the entry to database
            new_stock_entry.save()

            return redirect('portfolio_detail', pk)

    # Delete position
    if request.method == 'POST' and 'delete_position_button' in request.POST:
        Positions.objects.get(id=request.POST.get('id')).delete()
        # Check if remaining positions in portfolio
        portfolio.total_positions -= 1
        portfolio.save()
        return redirect('portfolio_detail', pk)

    # Edit position
    if request.method == 'POST' and 'edit_position_button' in request.POST:
        form = PositionForm(request.POST)
        if form.is_valid():
            # Getting all the cleaned data for the database entry
            user_input_stock_name = form.cleaned_data['ticker_name']
            user_input_buy_price = form.cleaned_data['buy_price']
            user_input_quantity = form.cleaned_data['quantity']
            user_input_market = form.cleaned_data['market']

            position_from_db = Positions.objects.get(id=request.POST.get('id'))
            position_from_db.ticker_name = user_input_stock_name
            position_from_db.buy_price = user_input_buy_price
            position_from_db.quantity = user_input_quantity
            position_from_db.market = user_input_market
            position_from_db.save()
        return redirect('portfolio_detail', pk)

    # Delete portfolio
    if request.method == 'POST' and 'delete_button' in request.POST:
        if Positions.objects.filter(portfolio=pk).exists() or Portfolio.objects.get(id=pk):
            Portfolio.objects.get(id=pk).delete()
            return redirect('stocktracker')

    return render(request, 'database-projects/portfolio_detail.html', context=context)


@login_required
def show_pdf_report_lab(request):
    # Create a file-like buffer to receive PDF data.
    pdf = core_pdf_generator.GeneratePdf()

    pdf.set_text('PLACEHOLDER FOR NOW')

    # Close the PDF object cleanly.
    pdf.show_page()
    pdf.save_page()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    pdf.data_buffer_for_pdf.seek(0)

    return FileResponse(pdf.data_buffer_for_pdf, as_attachment=False, filename='test.pdf')


@login_required
def download_portfolio_csv(request, request_id: int):
    portfolio = Portfolio.objects.get(id=request_id)
    positions = Positions.objects.filter(portfolio_id=request_id)
    generate_filename = f"{date.today()}/{portfolio.portfolio_name}"
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': f'attachment; filename="{generate_filename}.csv"'},
    )
    writer = csv.writer(response)
    headers = ['ID', 'Stockticker', 'Buy price', 'Quantity', 'Amount invested', 'Current market price', 'Profit',
               'Profit %']
    writer.writerow(headers)
    for position in positions:
        writer.writerow(
            [position.id, position.ticker_name, position.buy_price, position.quantity, position.amount_invested,
             position.current_market_price, position.position_profit, position.position_profit_in_percentage])

    return response
