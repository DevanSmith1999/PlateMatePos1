from django.urls import path
from django.urls import include
from .views import authView

urlpatterns = [
path("signup/", authView, name="authView"),
 path("accounts/", include("django.contrib.auth.urls")),
]