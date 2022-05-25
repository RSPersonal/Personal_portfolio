from django.urls import path
from . import views


urlpatterns = [
    path('', views.projects_overview, name='website_projects_overview'),
    path('real-estate-agent', views.real_estate_homepage, name='real_estate_homepage'),
    path('property/<int:property_id>', views.property_detail, name='property_detail'),
    path('sale-properties/all', views.sale_properties, name='sale_properties')
]
