import sentry_sdk
from django.contrib import messages
from typing import Any
from core.helpers_and_validators.iex_api import IexCloudAPI, check_active_connection
from .models import Portfolio, Positions
from core.helpers_and_validators import stock_calculator
from typing import List, Dict
from django.shortcuts import redirect



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
        stock_object = IexCloudAPI(ticker_symbol)
        try:
            price_from_stock_api = stock_object.get_stock_price()
        except KeyError as error:
            sentry_sdk.capture_exception(error)
            price_from_stock_api = 0
        except ConnectionError as e:
            sentry_sdk.capture_exception(e)
            price_from_stock_api = 0

        # Get current market price for profit calculation
        if not price_from_stock_api or price_from_stock_api == 0:
            messages.add_message(request, messages.INFO, 'error')
            return
        elif price_from_stock_api:
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


def save_portfolio_values_to_db(portfolio, calculated_profits):
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


def delete_portfolio(portfolio_id):
    # Delete portfolio
    if Positions.objects.filter(portfolio=portfolio_id).exists() or Portfolio.objects.get(id=portfolio_id):
        Portfolio.objects.get(id=portfolio_id).delete()
        return redirect('stocktracker')  # pragma: no cover
