import uuid
from django.db import models
from core.storage_backends import PublicMediaStorage, StaticStorage


# Create your models here.
class PropertyModel(models.Model):
    SALE = 'SL'
    RENTAL = 'RT'
    TYPE_OF_PROPERTY_CHOICES = [
        (SALE, 'Sale'),
        (RENTAL, 'Rental')
    ]
    street = models.CharField(max_length=50, blank=True, null=True)
    housenumber = models.IntegerField(blank=True, null=True)
    housenumber_add = models.CharField(max_length=15, blank=True, null=True)
    zipcode = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    municipality = models.CharField(max_length=60, blank=True, null=True)
    province = models.CharField(max_length=60, blank=True, null=True)
    type_of_property = models.CharField(blank=True, null=True, max_length=5, choices=TYPE_OF_PROPERTY_CHOICES, default=SALE)
    woon_oppervlak = models.IntegerField(default=0, blank=True, null=True)
    perceel_oppervlak = models.IntegerField(default=0, blank=True, null=True)
    amount_rooms = models.IntegerField(default=0, null=True)
    construction_year = models.IntegerField(blank=True, null=True)
    ask_price = models.CharField(max_length=30, default=0)
    description = models.TextField(blank=True, null=True)
    thumbnail_photo = models.FileField(blank=True, storage=PublicMediaStorage)
    other_photos = models.FileField(blank=True, storage=PublicMediaStorage)
    added_on = models.DateTimeField(auto_now=True)



