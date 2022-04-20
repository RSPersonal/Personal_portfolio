from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_overview, name='api_overview'),
    path('geo-api/get-ip', views.geo_api_get_ip, name='geo_api_get_ip'),
    path('currency-converter/', views.currency_converter_call, name='currency_converter_call'),
    path('keyword-finder/', views.keyword_finder),
    path('chart-data/', views.endpoint_chart_data),
    path('chart-data/<int:pk>', views.get_portfolio_monthly_profit),
]
