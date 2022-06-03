import uuid
from django.db import models
from core.storage_backends import PublicMediaStorage


# Create your models here.
class PropertyModel(models.Model):
    SALE = 'SL'
    RENTAL = 'RT'
    TYPE_OF_PROPERTY_CHOICES = [
        (SALE, 'Sale'),
        (RENTAL, 'Rental')
    ]

    TWO_UNDER_ONE = 'TOO'
    END_HOME = 'EH'
    TERRACES_HOUSE = 'TH'
    CORNER_HOUSE = 'COH'
    IN_BETWEEN_HOUSE = 'IBH'
    DETACHED_HOUSE = 'DH'
    APARTMENT = 'AP'
    NONE = 'NONE'

    BUILDING_TYPE_CHOICES = [
        (TWO_UNDER_ONE, '2-onder-1-kapwoning'),
        (END_HOME, 'Eindwoning'),
        (TERRACES_HOUSE, 'Geschakelde woning'),
        (CORNER_HOUSE, 'Hoekwoning'),
        (IN_BETWEEN_HOUSE, 'Tussenwoning'),
        (DETACHED_HOUSE, 'Vrijstaande woning'),
        (APARTMENT, 'Appartement'),
        (NONE, 'Onbekend'),
    ]

    SOLD = 'SD'
    UNDER_OFFER = 'UO'
    SOLD_WITH_RESERVATION = 'SWR'
    AVAILABLE = 'AV'

    STATUS_CHOICES = [
        (SOLD, 'Verkocht'),
        (UNDER_OFFER, 'Onder bod'),
        (SOLD_WITH_RESERVATION, 'Verkocht onder voorbehoud'),
        (AVAILABLE, 'Beschikbaar'),
        (NONE, 'Onbekend')
    ]

    property_id = models.UUIDField(default=uuid.uuid4)
    status = models.CharField(max_length=40, choices=STATUS_CHOICES, default=NONE, blank=True)
    street = models.CharField(max_length=50, blank=True, default="")
    housenumber = models.IntegerField(blank=True, null=True)
    housenumber_add = models.CharField(max_length=15, blank=True, default="")
    zipcode = models.CharField(max_length=10, blank=True, default="")
    city = models.CharField(max_length=100, blank=True, default="")
    municipality = models.CharField(max_length=60, blank=True, default="")
    province = models.CharField(max_length=60, blank=True, default="")
    type_of_property = models.CharField(blank=True, max_length=5, choices=TYPE_OF_PROPERTY_CHOICES,
                                        default=SALE)
    building_type = models.CharField(blank=True, max_length=20, choices=BUILDING_TYPE_CHOICES,
                                     default=NONE)
    woon_oppervlak = models.IntegerField(default=0, blank=True, null=True)
    perceel_oppervlak = models.IntegerField(default=0, blank=True, null=True)
    amount_rooms = models.IntegerField(default=0, null=True)
    energy_label = models.CharField(default="", blank=True, max_length=10)
    type_of_heating = models.CharField(default="", blank=True, max_length=20)
    construction_year = models.IntegerField(blank=True, null=True)
    ask_price = models.IntegerField(default=0)
    ask_price_suffix = models.CharField(max_length=10, blank=True, default="")
    description = models.TextField(blank=True, null=True)
    thumbnail_photo = models.FileField(blank=True, storage=PublicMediaStorage)
    other_photos = models.FileField(blank=True, storage=PublicMediaStorage)
    added_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} {} {} {} {}'.format(self.street, self.zipcode, self.city, self.province, self.description)
