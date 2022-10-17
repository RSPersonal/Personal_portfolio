from django.urls import path
from . import views

urlpatterns = [
    path('', views.projects_overview, name='website_projects_overview'),
    path('real-estate-agent', views.real_estate_homepage, name='real_estate_homepage'),
    path('real-estate-agent/property/<int:property_id>', views.property_detail, name='property_detail'),
    path('real-estate-agent/sale-properties/all', views.sale_properties, name='sale_properties'),
    path('real-estate-agent/rental-properties/all', views.rental_properties, name='rental_properties'),
    path('real-estate-agent/services/', views.real_estate_services, name='real_estate_services'),
    path('real-estate-agent/valuation', views.real_estate_valuation, name='real_estate_valuation'),
    path('real-estate-agent/sale-service', views.real_estate_sale_service, name='real_estate_sale_service'),
]
