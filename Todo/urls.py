from django.urls import path
from django.urls.conf import include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'todos', views.TodoViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include('rest_framework.urls', namespace="rest_framework")),
    path("todo/add", views.create_form, name='todo_form'),
    path("update/<int:pk>", views.update_todo, name='todo_update_form'),
    path("all-todos/", views.overview_to_dos, name='todo_index'),
]
