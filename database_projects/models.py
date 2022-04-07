from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField


# Create your models here.
class Portfolio(models.Model):
    portfolio_name = models.CharField(max_length=50)
    created_on = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    total_amount_invested = models.FloatField(default=0)
    total_profit = models.FloatField(default=0)
    total_profit_percentage = models.FloatField(default=0.0)
    total_positions = models.IntegerField(default=0.0)
    labels_array = ArrayField(models.CharField(max_length=20, default=''))
    data_for_chart_array = ArrayField(models.FloatField(default=0.0))
    monthly_profit = ArrayField(models.FloatField(default=0.0))

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


class MotivationLetterModel(models.Model):
    motivation_letter_body = models.TextField(default='')
    created_on = models.DateTimeField(auto_now=True)
    firm_name = models.CharField(max_length=50, default='')
