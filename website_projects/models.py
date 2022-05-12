from django.db import models


# Create your models here.
class PropertyModel(models.Model):
    street = models.CharField(max_length=50)
    housenumber = models.IntegerField(blank=True, null=True)
    housenumber_add = models.CharField(max_length=15)
    zipcode = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    municipality = models.CharField(max_length=60)
    province = models.CharField(max_length=60)
    ask_price = models.FloatField()
    construction_year = models.IntegerField(blank=True, null=True)
    amount_rooms = models.IntegerField(default=0, null=True)
    description = models.TextField()
