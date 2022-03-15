import numpy as np


def calculate_stock_profit(price_bought, current_market_price, quantity):
    """
    Function to calculate the current profit for the stock position
    """
    return np.subtract((current_market_price * quantity), (price_bought * quantity))


