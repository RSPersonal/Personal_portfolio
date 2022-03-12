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
    type = models.CharField(max_length=20)
    buy_price = models.FloatField()
    market = models.CharField(max_length=20)
    quantity = models.FloatField(default=1)
    portfolio = models.ForeignKey('Portfolio', on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} {} {}'.format(self.ticker_name, self.type, self.market)
