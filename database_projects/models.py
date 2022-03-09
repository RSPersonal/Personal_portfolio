from django.db import models


# Create your models here.
class Portfolio(models.Model):
    portfolio_name = models.CharField(max_length=50)

    def __str__(self):
        return self.portfolio_name


class Positions(models.Model):
