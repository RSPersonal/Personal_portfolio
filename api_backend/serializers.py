from rest_framework import serializers
from database_projects.models import Portfolio
from website_projects.models import PropertyModel


class PortfolioSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    monthly_profit = serializers.ListField(child=serializers.FloatField())

    class Meta:
        model = Portfolio
        fields = ['id', 'user', 'monthly_profit']


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyModel
        fields = ('id', 'street', 'housenumber', 'housenumber_add', 'zipcode', 'city', 'municipality', 'province',
                  'type_of_property')

        # woon_oppervlak = models.IntegerField(default=0, blank=True, null=True)
        # perceel_oppervlak = models.IntegerField(default=0, blank=True, null=True)
        # amount_rooms = models.IntegerField(default=0, null=True)
        # construction_year = models.IntegerField(blank=True, null=True)
        # ask_price = models.CharField(max_length=30, default=0)
        # description = models.TextField(blank=True, null=True)
        # thumbnail_photo = models.FileField(blank=True, storage=PublicMediaStorage)
        # other_photos = models.FileField(blank=True, storage=PublicMediaStorage)
        # added_on = models.DateTimeField(auto_now=True)
