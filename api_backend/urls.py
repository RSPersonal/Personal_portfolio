from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_overview, name='api_overview'),
    path('geo-api', views.geo_api_get_ip, name='geo_api_get_ip')
]
