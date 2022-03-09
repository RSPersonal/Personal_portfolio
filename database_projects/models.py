from django.db import models


# Create your models here.
class Portfolio(models.Model):
    portfolio_name = models.CharField(max_length=50)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.portfolio_name


class Positions(models.Model):
    ticker_name = models.CharField(max_length=40)
    type = models.CharField(max_length=20)
    buy_price = models.FloatField()
    market = models.CharField(max_length=20)
    portfolio = models.ForeignKey('Portfolio', on_delete=models.CASCADE)
    added_on = models.DateTimeField()

    def __str__(self):
        return '{} {} {}'.format(self.ticker_name, self.type, self.market)
