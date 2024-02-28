from django.urls import path
from PlateMate import views

urlpatterns = [
    path("", views.home, name="home"),
]