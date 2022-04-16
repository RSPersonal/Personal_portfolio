from rest_framework import serializers
from database_projects.models import Portfolio


class PortfolioSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    monthly_profit = serializers.ListField(child=serializers.FloatField())

    class Meta:
        model = Portfolio
        fields = ['id', 'user', 'monthly_profit']

