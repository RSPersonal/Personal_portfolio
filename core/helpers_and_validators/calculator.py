import numpy as np


def calculate_stock_profit(price_bought: float, current_market_price: float, quantity: float):
    """
    @param price_bought: float
    @param current_market_price: float
    @param quantity: float
    @return: calculated profit
    """
    return np.subtract((current_market_price * quantity), (price_bought * quantity))


def calculate_total_amount_invested(buy_price: float, amount_of_stocks: float):
    """
    @param buy_price:
    @param amount_of_stocks:
    @return: buy_price * amount_of_stocks
    """
    return np.multiply(buy_price, amount_of_stocks)


def calculate_profit_in_percentage(buy_price: float, quantity: float, profit: float):
    """
    @param buy_price:
    @param quantity:
    @param profit:
    @return: profit / (buy_price * quantity)
    """
    calculated_total_amount_invested = calculate_total_amount_invested(buy_price, quantity)
    return round(np.divide(profit, calculated_total_amount_invested) * 100, 2)


def calculate_portfolio_profit_in_percentage(amount_invested: float, profit: float):
    """
    @param amount_invested:
    @param profit:
    @return: profit / (buy_price * quantity)
    """

    return round(np.divide(profit, amount_invested) * 100, 2)


def calculate_mean_price(prices: list):
    """
    @param prices: list
    @return: mean price from list
    """
    return np.mean(prices)
