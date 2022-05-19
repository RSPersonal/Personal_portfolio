from django.urls import path
from . import views


urlpatterns = [
    path('', views.projects_overview, name='website_projects_overview'),
    path('real-estate-agent', views.real_estate_example, name='real_estate_example'),
    path('property/<int:property_id>', views.property_detail, name='property_detail')
]
