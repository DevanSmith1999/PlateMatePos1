from django.urls import path
from django.urls import include
from .views import signup


urlpatterns = [
path("signup/", signup, name="authView"),
 path("accounts/", include("django.contrib.auth.urls")),
]