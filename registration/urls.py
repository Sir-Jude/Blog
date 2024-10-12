from django.contrib.auth import views as auth_views
from django.urls import path
from . import views


app_name = "registration"
urlpatterns = [
    path("register/", views.UserRegisterView.as_view(), name="register"),
]
