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
from database_projects import services


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
    limit_exceeded = False  # stock_api.check_if_limit_exceeded()  # pragma: no cover
    active_connection = check_active_connection()  # pragma: no cover
    debug = os.getenv("DEBUG", config("DEBUG"))  # pragma: no cover
    portfolio = Portfolio.objects.get(id=pk)
    position_form = PositionForm()

    # Here we need the correct ip for the api call to get the daily return
    if debug == 'False':
        api_host_ip = os.getenv("API_HOST_PROD", config("API_HOST_PROD"))  # pragma: no cover
    else:
        api_host_ip = os.getenv("API_HOST_LOCAL", config("API_HOST_LOCAL"))  # pragma: no cover

    context = {'position_form': position_form, 'portfolio': portfolio,
               'labels_monthly': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov',
                                  'Dec'], 'api_host': api_host_ip}

    # First check if there are any active positions
    positions = services.check_if_active_positions_and_calculate_current_profits(request, portfolio, pk,
                                                                                 active_connection, limit_exceeded)
    if positions:
        context['positions'] = positions

    # Adding new positions to database
    # TODO Redirect currently does not refresh the positions after adding a new position
    services.add_new_stock_entry(request, portfolio, pk, active_connection, limit_exceeded)

    # Delete position
    services.delete_position(request, portfolio, pk)

    # Edit position
    if request.method == 'POST' and 'edit_position_button' in request.POST:
        valid_form = services.validate_position_form(request)
        user_input_form = PositionForm(request.POST)

        if valid_form:
            clean_position = services.get_clean_form_data(user_input_form,
                                                          ['ticker_name', 'buy_price', 'quantity', 'market'])
            services.update_stock_entry(request, clean_position)

        return redirect('portfolio_detail', pk)  # pragma: no cover

    # Delete Portfolio
    services.delete_portfolio(request, pk)

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
