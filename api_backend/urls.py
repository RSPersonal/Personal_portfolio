from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_overview, name='api_overview'),
    path('geo-api/get-ip', views.geo_api_get_ip, name='geo_api_get_ip'),
    path('currency-converter/', views.currency_converter_call, name='currency_converter_call'),
    path('keyword-finder/', views.keyword_finder, name='keyword_finder'),
    path('chart-data/', views.endpoint_chart_data, name='chart_data_endpoint'),
    path('chart-data/<int:pk>', views.get_portfolio_monthly_profit, name="chart_data_id"),
    path('properties/sale/<str:user_input_city>', views.get_user_desired_properties, name="properties_sale"),
    path('tasks/all', views.get_all_tasks, name="get_all_tasks"),
    path('task/<int:pk>', views.task_detail, name="tasks_detail"),
    path('visitor-count', views.get_visitor_count, name="get_visitor_count")
]
