from django.urls import path
from . import views

urlpatterns = [
    path('', views.database_homepage, name='database-projects'),
    path('-stocktracker/', views.stock_tracker_landing_page, name='stocktracker'),
    path('-stocktracker/portfolio/<int:pk>', views.portfolio_detail, name='portfolio_detail')
]
