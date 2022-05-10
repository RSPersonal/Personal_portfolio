from django.urls import path
from . import views


urlpatterns = [
    path("", views.home_page_en, name="homepage_en"),
    path("nl", views.home_page_nl, name="homepage_nl"),
    path("contact", views.contact, name="contact_page"),
]
