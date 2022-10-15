import sentry_sdk
import uuid
from django.contrib import messages
from typing import Any
from django.http import HttpResponse

from core.helpers_and_validators.iex_api import IexCloudAPI, check_active_connection
from .models import Portfolio, Positions
from core.helpers_and_validators import stock_calculator
from typing import List, Dict
from django.shortcuts import redirect
from .forms import PortfolioForm, PositionForm


def check_if_active_positions(portfolio_id: Any) -> bool:
    """
    @param portfolio_id:
    @return: Object containing Portfolio or None
    """
    if Positions.objects.filter(portfolio=portfolio_id).exists():
        return True
    return False


def get_all_positions_in_portfolio(portfolio_id: int) -> Any:
    """
    @param portfolio_id:
    @return: Query object with all positions
    """
    return Positions.objects.filter(portfolio=portfolio_id).order_by('added_on')


def calculate_position_and_position_profit(request, positions):
    """
    @param request:
    @param positions:
    @return:
    """

    current_market_price_from_api_call: float | int = 0
    calculated_total_amount_invested_in_portfolio: float | int = 0
    calculated_total_profit_portfolio: float | int = 0
    calculated_total_profit_percentage: float = 0.0
    calculated_total_positions: int = 0
    labels_for_portfolio_chart: List[str] = []
    data_for_portfolio_chart: List[int | float] = []
    calculated_positions: List[Dict] = []
    position_object: Dict = {
        'symbol': None,
        'calculated_profit': None,
        'calculated_total_invested': None,
        'current_market_price_from_api_call': None,
    }

    for position in positions:
        ticker_symbol = position.ticker_name

        # Get stock data
        price_from_stock_api = 0
        try:
            stock_object = IexCloudAPI(ticker_symbol)
            if stock_object.valid_stock:
                price_from_stock_api = stock_object.latest_stock_price
        except KeyError as error:
            sentry_sdk.capture_exception(error)
        except ConnectionError as e:
            sentry_sdk.capture_exception(e)
        except TypeError as e:
            sentry_sdk.capture_exception(e)

        # Get current market price for profit calculation
        if price_from_stock_api:
            position.current_market_price = price_from_stock_api
            current_market_price_from_api_call = price_from_stock_api
        else:
            position.current_market_price = 0
            current_market_price_from_api_call = 0

        # Total amount invested calculation
        calculated_total_invested = stock_calculator.calculate_total_amount_invested(position.buy_price,
                                                                                     position.quantity)
        calculated_total_amount_invested_in_portfolio += calculated_total_invested

        # Profit calculation
        if position.current_market_price == 0:
            calculated_profit = 0
        else:
            calculated_profit = stock_calculator.calculate_stock_profit(position.buy_price,
                                                                        current_market_price_from_api_call,
                                                                        position.quantity)
        calculated_total_profit_portfolio += calculated_profit

        # Profit in percentage calculation
        calculated_profit_perc = stock_calculator.calculate_profit_in_percentage(position.buy_price,
                                                                                 position.quantity,
                                                                                 calculated_profit)
        calculated_total_profit_percentage += calculated_profit_perc

        # Total positions
        calculated_total_positions += 1

        labels_for_portfolio_chart.append(ticker_symbol)

        # Data for Portfolio chart
        data_for_portfolio_chart.append(position.quantity)

        # Save some to the position model
        position.position_profit_in_percentage = calculated_profit_perc
        position.amount_invested = round(calculated_total_invested, 2)
        position.position_profit = round(calculated_profit, 2)
        position.position_profit_in_percentage = round(calculated_profit_perc, 2)
        position.save()

        position_object['symbol'] = ticker_symbol
        position_object['calculated_profit'] = calculated_profit
        position_object['calculated_total_invested'] = calculated_total_invested
        position_object['current_market_price_from_api_call'] = current_market_price_from_api_call

        calculated_positions.append(position_object)
        position_object = {
            'symbol': None,
            'calculated_profit': None,
            'calculated_total_invested': None,
            'current_market_price_from_api_call': None,
        }

    return {
        'calculated_positions': calculated_positions,
        'calculated_total_amount_invested_in_portfolio': calculated_total_amount_invested_in_portfolio,
        'calculated_total_profit_portfolio': calculated_total_profit_portfolio,
        'calculated_total_profit_percentage': calculated_total_profit_percentage,
        'calculated_total_positions': calculated_total_positions,
        'labels_for_portfolio_chart': labels_for_portfolio_chart,
        'data_for_portfolio_chart': data_for_portfolio_chart
    }


def save_portfolio_values_to_db(portfolio, calculated_profits) -> None:
    """
    @param portfolio:
    @param calculated_profits:
    @return:
    """
    portfolio.total_positions = calculated_profits['calculated_total_positions']
    portfolio.total_amount_invested = calculated_profits['calculated_total_amount_invested_in_portfolio']
    portfolio.total_profit = round(calculated_profits['calculated_total_profit_portfolio'], 2)
    portfolio.total_profit_percentage = stock_calculator.calculate_portfolio_profit_in_percentage(
        calculated_profits['calculated_total_amount_invested_in_portfolio'],
        calculated_profits['calculated_total_profit_portfolio'])
    portfolio.labels_array = calculated_profits['labels_for_portfolio_chart']
    portfolio.data_for_chart_array = calculated_profits['data_for_portfolio_chart']
    portfolio.save()


def delete_portfolio(request, portfolio_id) -> HttpResponse:
    """
    @param request:
    @param portfolio_id:
    @return:
    """
    # Delete portfolio
    if request.method == 'POST' and 'delete_button' in request.POST:
        if Positions.objects.filter(portfolio=portfolio_id).exists() or Portfolio.objects.get(id=portfolio_id):
            Portfolio.objects.get(id=portfolio_id).delete()
        return redirect('stocktracker')  # pragma: no cover


def update_stock_entry(request, clean_user_input_position: Dict) -> None:
    """
    @param request:
    @param clean_user_input_position: Dictionary container the cleaned and valid input from user
    @return:
    """
    position_from_db = Positions.objects.get(id=request.POST.get('id'))
    position_from_db.ticker_name = clean_user_input_position['ticker_name']
    position_from_db.buy_price = clean_user_input_position['buy_price']
    position_from_db.quantity = clean_user_input_position['quantity']
    position_from_db.market = clean_user_input_position['market']
    position_from_db.save()


def get_clean_form_data(form_object, desired_fields: List[str]) -> Dict:
    clean_fields = {}
    if form_object.is_valid():
        for field in desired_fields:
            clean_fields[field] = form_object.cleaned_data[field]
    return clean_fields


def validate_position_form(request) -> bool:
    """
    @param request:
    @return:
    """
    form = PositionForm(request.POST)
    if form.is_valid():
        return True
    return False


def add_stock_entry(portfolio_instance, clean_position) -> None:
    """
    @param portfolio_instance:
    @param clean_position:
    @return:
    """
    # TODO Maybe implement the validation for the clean_position dictionary.
    new_stock_entry = Positions(pk=uuid.uuid4(), portfolio=portfolio_instance,
                                ticker_name=clean_position['ticker_name'],
                                buy_price=clean_position['buy_price'],
                                current_market_price=clean_position['buy_price'],
                                quantity=clean_position['quantity'],
                                market=clean_position['market']
                                )
    new_stock_entry.save()
    return None


def get_current_stock_market_price(stock_name: str) -> float | int:
    try:
        stock_object = IexCloudAPI(stock_name)
        response_stock_data_json = stock_object.stock_json
        if response_stock_data_json and stock_object.stock_symbol == stock_name:
            current_market_price_from_api_call_or_zero = stock_object.latest_stock_price
        else:
            current_market_price_from_api_call_or_zero = 0
    except ConnectionError as e:
        sentry_sdk.capture_exception(e)
        current_market_price_from_api_call_or_zero = 0
    except KeyError as e:
        sentry_sdk.capture_exception(e)
        current_market_price_from_api_call_or_zero = 0
    return current_market_price_from_api_call_or_zero


def add_new_stock_entry(request, portfolio_instance, portfolio_id, active_connection: bool, limit_exceeded: bool):
    """
    @param request: request object
    @param portfolio_instance: Portfolio instance
    @param portfolio_id: UUID
    @param active_connection: Bool
    @param limit_exceeded:  Bool
    @return: None | Redirect
    """
    if request.method == 'POST' and 'add_position_button' in request.POST:
        if not active_connection:
            messages.add_message(request, messages.INFO, 'No api connection.')
            return redirect('portfolio_detail', portfolio_id)  # pragma: no cover
        elif limit_exceeded:
            messages.add_message(request, messages.INFO, 'API CALL LIMIT EXCEEDED.')
            return redirect('portfolio_detail', portfolio_id)  # pragma: no cover

        add_position_form = PositionForm(request.POST)
        valid_form = validate_position_form(request)

        if valid_form:
            found_stock = False
            clean_position = get_clean_form_data(add_position_form,
                                                 ['ticker_name', 'buy_price', 'quantity', 'market'])
            current_stock_market_price = get_current_stock_market_price(clean_position['ticker_name'])
            clean_position['current_stock_market_price'] = current_stock_market_price

            if current_stock_market_price:
                add_stock_entry(portfolio_instance, clean_position)
                found_stock = True
                return redirect('portfolio_detail', portfolio_id)  # pragma: no cover

            if not found_stock:
                messages.add_message(request, messages.INFO, "Could not find Stock, make sure you spelled it correct")
            return redirect('portfolio_detail', portfolio_id)  # pragma: no cover
    return None


def check_if_active_positions_and_calculate_current_profits(request, portfolio_instance, portfolio_id,
                                                            active_connection: bool, limit_exceeded: bool):
    """
    @param request:
    @param portfolio_instance:
    @param portfolio_id: UUID
    @param active_connection: Bool
    @param limit_exceeded: Bool
    @return: None | Query set [Calculated Positions]
    """
    calculated_positions = None
    if check_if_active_positions(portfolio_id):
        positions = get_all_positions_in_portfolio(portfolio_id)
        if active_connection:
            if not limit_exceeded:
                calculated_positions_profit = calculate_position_and_position_profit(request, positions)
                # Save it to the portfolio object to show later in portfolio overview
                if calculated_positions_profit:
                    save_portfolio_values_to_db(portfolio_instance, calculated_positions_profit)
                    calculated_positions = positions
            else:
                messages.add_message(request, messages.INFO,
                                     'API call limit exceeded. Profit calculation is up to date due to market price is\
                                     set to last retrieved market price in case of api call limit is exceeded.')
        else:
            messages.add_message(request, messages.INFO, 'No active connection, check if API key is valid.')
    return calculated_positions


def delete_position(request, portfolio_instance, portfolio_id):
    """
    @param request:
    @param portfolio_instance:
    @param portfolio_id: UUID
    @return: None
    """
    if request.method == 'POST' and 'delete_position_button' in request.POST:
        position = Positions.objects.get(id=request.POST.get('id'))
        # Check if remaining positions in portfolio
        portfolio_instance.total_positions -= 1
        portfolio_instance.total_profit = portfolio_instance.total_profit - position.position_profit
        position.delete()

        portfolio_instance.save()
        return redirect('portfolio_detail', portfolio_id)  # pragma: no cover
    return None