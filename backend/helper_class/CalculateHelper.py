import numpy as np


def calculate_stock_profit(price_bought: float, current_market_price: float, quantity: float):
    """
    @param price_bought: float
    @param current_market_price: float
    @param quantity: float
    @return:
    """
    return np.subtract((current_market_price * quantity), (price_bought * quantity))


def calculate_total_amount_invested(buy_price: float, amount_of_stocks: float):
    """
    @param buy_price:
    @param amount_of_stocks:
    @return:
    """
    return np.multiply(buy_price, amount_of_stocks)


def calculate_profit_in_percentage(buy_price: float, quantity: float, profit: float):
    """
    @param buy_price:
    @param quantity:
    @param profit:
    @return:
    """
    calculated_total_amount_invested = calculate_total_amount_invested(buy_price, quantity)

    return round(np.divide(profit, calculated_total_amount_invested) * 100, 2)
