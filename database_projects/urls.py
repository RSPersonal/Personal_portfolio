from django.urls import path
from . import views

urlpatterns = [
    path('', views.database_homepage, name='database-projects')
]
