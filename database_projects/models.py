from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Portfolio(models.Model):
    portfolio_name = models.CharField(max_length=50)
    created_on = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.portfolio_name


class Positions(models.Model):
    ticker_name = models.CharField(max_length=40)
    buy_price = models.FloatField()
    current_market_price = models.FloatField()
    market = models.CharField(max_length=20)
    quantity = models.FloatField(default=1)
    amount_invested = models.FloatField(default=0)
    position_profit = models.FloatField(default=0.0)
    position_profit_in_percentage = models.FloatField(default=0.0)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} {}'.format(self.ticker_name, self.market)
