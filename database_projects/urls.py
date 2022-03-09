from django.urls import path
from . import views

urlpatterns = [
    path('', views.database_homepage, name='database-projects'),
    path('-stocktracker/', views.stock_tracker, name='stocktracker')
]
