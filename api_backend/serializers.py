from rest_framework import serializers, viewsets
from database_projects.models import Portfolio
from website_projects.models import PropertyModel
from homepage.models import VisitorCount
from homepage.models import ProfilePosts
from .models import Task


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


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'completed', 'created_at']


class VisitorCountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VisitorCount
        fields = ['visitor_count']


class ProfilePostsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProfilePosts
        fields = ['post', 'order', 'language']
