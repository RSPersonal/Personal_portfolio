from django.urls import path
from . import views

urlpatterns = [
    path('', views.database_homepage, name='database-projects'),
    path('-stocktracker/', views.stock_tracker_landing_page, name='stocktracker'),
    path('-stocktracker/portfolio/<int:pk>', views.portfolio_detail, name='portfolio_detail'),
    path('-stocktracker/portfolio/report-lab/pdf', views.show_pdf_report_lab),
    path('-stocktracker/portfolio/csv/<int:request_id>', views.download_portfolio_csv),
    path('-valuation-tool/', views.valuation_tool, name="valuation_tool")
]
