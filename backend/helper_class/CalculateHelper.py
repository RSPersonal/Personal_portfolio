import numpy as np


def calculate_stock_profit(price_bought: float, current_market_price: float, quantity: float):
    """
    @param price_bought: float
    @param current_market_price: float
    @param quantity: float
    @return:
    """
    return np.subtract((current_market_price * quantity), (price_bought * quantity))


def calculate_profit_in_percentage(price_bought: float, current_market_price: float, quantity: float):
    """
    @param price_bought:
    @param current_market_price:
    @param quantity:
    @return:
    """
