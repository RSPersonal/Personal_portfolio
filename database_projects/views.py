import csv
import os
import random
import uuid
from datetime import date
from datetime import datetime

import requests
import sentry_sdk
from decouple import config
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, HttpResponse
from django.shortcuts import render, redirect

from core.core_pdf_generator import core_pdf_generator
from core.helpers_and_validators import input_validator
from core.helpers_and_validators.extraction_helper import extract_postal_code
from core.helpers_and_validators import stock_calculator
from core.helpers_and_validators.iex_api import IexCloudAPI, check_active_connection
from core.helpers_and_validators.valuation_service import get_properties_within_postal_code_range_and_nla_range, \
    get_mean_property_price
from .forms import PortfolioForm, PositionForm
from .models import Portfolio, Positions


# Create your views here
def database_homepage(request):
    context = {}
    return render(request, 'database-projects/database-projects.html', context=context)  # pragma: no cover


@login_required
def stock_tracker_landing_page(request):
    # Getting all portfolio's from user
    current_user_id = request.user.id
    portfolio_or_portfolios = Portfolio.objects.filter(user_id=current_user_id)
    context = {}
    portfolio_form = PortfolioForm()

    context['portfolios'] = portfolio_or_portfolios
    context['portfolio_form'] = portfolio_form
    context['labels_monthly'] = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']

    #  Adding the total profit to correct month.
    current_month = datetime.now()
    current_month_for_data_array = (current_month.month - 1)

    # TODO Write test for adding portfolio and adding the profit to the correct month
    for portfolio in portfolio_or_portfolios:
        # Don't execute the save if the id is already stored
        if portfolio.id_for_chart == '':
            portfolio.id_for_chart = str(portfolio.id).replace('-', '')

        try:
            portfolio.monthly_profit[current_month_for_data_array] = portfolio.total_profit
            portfolio.save()
        except KeyError as error:
            sentry_sdk.capture_exception(error)
        except IndexError as error:
            sentry_sdk.capture_exception(error)
            portfolio.monthly_profit.append(0)
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

            cleaned_user_portfolio_name = form.cleaned_data['portfolio_name']
            new_portfolio_entry = Portfolio(portfolio_name=cleaned_user_portfolio_name,
                                            user_id=request.user.id,
                                            data_for_chart_array=[],
                                            labels_array=[],
                                            monthly_profit=monthly_profit_array_until_current_month
                                            )
            new_portfolio_entry.save()
    return render(request, 'database-projects/stocktracker.html', context=context)  # pragma: no cover


@login_required
def portfolio_detail(request, pk):
    # General checks for api calls
    # TODO Build check for IEX CLoud limit exceeded check
    limit_exceeded = False  # stock_api.check_if_limit_exceeded()  # pragma: no cover
    active_connection = check_active_connection()  # pragma: no cover
    demo_stock_prices = os.getenv("DEMO_MARKET_PRICES", config("DEMO_MARKET_PRICES"))  # pragma: no cover
    debug = os.getenv("DEBUG", config("DEBUG"))  # pragma: no cover
    if debug == 'False':
        api_host_ip = os.getenv("API_HOST_PROD", config("API_HOST_PROD"))  # pragma: no cover
    else:
        api_host_ip = os.getenv("API_HOST_LOCAL", config("API_HOST_LOCAL"))  # pragma: no cover
    print(api_host_ip)
    portfolio = Portfolio.objects.get(id=pk)
    position_form = PositionForm()

    context = {'position_form': position_form, 'portfolio': portfolio,
               'labels_monthly': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov',
                                  'Dec'], 'api_host': api_host_ip}

    # Here we need the correct ip for the api call to get the daily return

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

        if active_connection:
            if not limit_exceeded:
                for position in positions:
                    ticker_symbol = position.ticker_name

                    # Get stock data
                    if demo_stock_prices == 'False':
                        stock_object = IexCloudAPI(ticker_symbol)

                        try:
                            # price_from_stock_api = stock_api.get_stock_price(ticker_symbol)
                            price_from_stock_api = stock_object.get_stock_price()
                        except KeyError as error:
                            sentry_sdk.capture_exception(error)
                            price_from_stock_api = 0
                        except ConnectionError as e:
                            sentry_sdk.capture_exception(e)
                            price_from_stock_api = 0
                    else:
                        price_from_stock_api = random.randrange(0, 200)

                    # Get current market price for profit calculation
                    if limit_exceeded is False and input_validator.no_value(price_from_stock_api):
                        messages.add_message(request, messages.INFO, 'error')
                        break
                    elif input_validator.value(price_from_stock_api) and limit_exceeded is False:
                        position.current_market_price = price_from_stock_api
                        current_market_price_from_api_call = price_from_stock_api
                    else:
                        position.current_market_price = 0
                        current_market_price_from_api_call = 0

                    # Total amount invested calculation
                    calculated_total_invested = stock_calculator.calculate_total_amount_invested(position.buy_price,
                                                                                                 position.quantity)
                    position.amount_invested = calculated_total_invested
                    calculated_total_amount_invested_in_portfolio += calculated_total_invested

                    # Profit calculation
                    if position.current_market_price == 0:
                        calculated_profit = 0
                    else:
                        calculated_profit = stock_calculator.calculate_stock_profit(position.buy_price,
                                                                                    current_market_price_from_api_call,
                                                                                    position.quantity)
                    position.position_profit = round(calculated_profit, 2)
                    calculated_total_profit_portfolio += calculated_profit

                    # Profit in percentage calculation
                    calculated_profit_perc = stock_calculator.calculate_profit_in_percentage(position.buy_price,
                                                                                             position.quantity,
                                                                                             calculated_profit)
                    calculated_total_profit_percentage += calculated_profit_perc
                    position.position_profit_in_percentage = calculated_profit_perc

                    # Total positions
                    calculated_total_positions += 1

                    # Labels for Portfolio chart
                    if limit_exceeded is False:
                        labels_for_portfolio_chart.append(ticker_symbol)

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
                portfolio.total_profit_percentage = stock_calculator.calculate_portfolio_profit_in_percentage(
                    calculated_total_amount_invested_in_portfolio, calculated_total_profit_portfolio)
                portfolio.labels_array = labels_for_portfolio_chart
                portfolio.data_for_chart_array = data_for_portfolio_chart
                portfolio.save()
                context['positions'] = positions
            else:
                messages.add_message(request, messages.INFO, 'Development mode on, prices are random!')
                messages.add_message(request, messages.INFO,
                                     'API call limit exceeded. Profit calculation is up to date due to market price is\
                                     set to last retrieved market price in case of api call limit is exceeded.')
        else:
            messages.add_message(request, messages.INFO, 'No active connection, check if API key is valid.')
        context['positions'] = positions

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

            stock_object = IexCloudAPI(user_input_add_form_stock_name)
            active_connection = check_active_connection()
            if active_connection and limit_exceeded is False:
                response_stock_data_json = stock_object.stock_json
                if input_validator.value(response_stock_data_json) \
                        and stock_object.stock_symbol == user_input_add_form_stock_name:
                    found_stock = True
                    current_market_price_from_api_call_or_zero = stock_object.latest_stock_price
                else:
                    current_market_price_from_api_call_or_zero = 0
            else:
                current_market_price_from_api_call_or_zero = 0

            if limit_exceeded:
                messages.add_message(request, messages.INFO, 'API CALL LIMIT EXCEEDED.')
            elif found_stock is False:
                messages.add_message(request, messages.INFO, "Could not find Stock, make sure you spelled it correct")

            # Adding new entry to Database
            new_stock_entry = Positions(pk=uuid.uuid4(), portfolio=portfolio,
                                        ticker_name=user_input_add_form_stock_name,
                                        buy_price=user_input_add_form_buy_price,
                                        current_market_price=current_market_price_from_api_call_or_zero,
                                        quantity=user_input_add_form_quantity,
                                        market=user_input_add_form_market)
            # Saving the entry to database
            new_stock_entry.save()

            return redirect('portfolio_detail', pk)  # pragma: no cover

    # Delete position
    if request.method == 'POST' and 'delete_position_button' in request.POST:
        Positions.objects.get(id=request.POST.get('id')).delete()
        # Check if remaining positions in portfolio
        portfolio.total_positions -= 1
        portfolio.save()
        return redirect('portfolio_detail', pk)  # pragma: no cover

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
        return redirect('portfolio_detail', pk)  # pragma: no cover

    # Delete portfolio
    if request.method == 'POST' and 'delete_button' in request.POST:
        if Positions.objects.filter(portfolio=pk).exists() or Portfolio.objects.get(id=pk):
            Portfolio.objects.get(id=pk).delete()
            return redirect('stocktracker')  # pragma: no cover

    return render(request, 'database-projects/portfolio_detail.html', context=context)  # pragma: no cover


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

    return FileResponse(pdf.data_buffer_for_pdf, as_attachment=False, filename='test.pdf')  # pragma: no cover


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

    return response  # pragma: no cover


def valuation_tool(request):
    context = {'google_places_key': os.getenv('GOOGLE_PLACES_API', config('GOOGLE_PLACES_API'))}
    if request.method == 'POST' and 'searchAddressSubmitButton' in request.POST:
        # TODO expand test for input of user
        # TODO test should contain following cases: no input, mean price calculation
        user_input_nla = int(request.POST.get('nla'))
        user_input_city = request.POST.get('locality')
        user_input_type_of_object = request.POST.get('typeOfObject')
        clean_postal_code = extract_postal_code(request.POST.get('postcode'))
        user_input_radius = int(request.POST.get('radius'))
        try:
            postal_code_range = requests.get(
                f"http://postcode.vanvulpen.nl/afstand/{clean_postal_code}/{user_input_radius}/").json()
        except ConnectionError as e:
            sentry_sdk.capture_exception(e)
            postal_code_range = None

        # Makes no sense to search for properties if we have no postal code range
        if postal_code_range:
            queried_properties = get_properties_within_postal_code_range_and_nla_range(postal_code_range,
                                                                                       user_input_type_of_object,
                                                                                       user_input_nla, user_input_city)
            calculated_mean_property_price = get_mean_property_price(queried_properties)

            if len(queried_properties) > 0:
                context['found_objects'] = len(queried_properties)
            else:
                context['no_objects_found'] = True
            if calculated_mean_property_price:
                context['final_calculated_mean_price'] = calculated_mean_property_price
            else:
                context['final_calculated_mean_price'] = 0.0
            context['found_properties'] = queried_properties

        context['user_input_postal_code'] = clean_postal_code
        context['user_input_city'] = user_input_city
    return render(request, 'database-projects/valuation_tool.html', context=context)  # pragma:: no cover
