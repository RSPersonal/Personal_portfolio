from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_page, name="home_page"),
    path("aboutme", views.about_me, name="about_me"),
    path("contact", views.contact, name="contact")
]
