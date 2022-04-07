from rest_framework import serializers
from database_projects.models import Portfolio, MotivationLetter


class PortfolioSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    monthly_profit = serializers.ListField(child=serializers.FloatField())

    class Meta:
        model = Portfolio
        fields = ['id', 'user', 'monthly_profit']


class MotivationLetterSerializer(serializers.ModelSerializer):
    firm_name = serializers.CharField(read_only=True)
    motivation_letter_body = serializers.CharField(read_only=True)

    class Meta:
        model = MotivationLetter
        fields = ['firm_name', 'motivation_letter_body']
