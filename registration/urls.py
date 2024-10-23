from django.contrib.auth import views as auth_views
from django.urls import path
from . import views


app_name = "registration"
urlpatterns = [
    path("register/", views.UserRegisterView.as_view(), name="register"),
    path("edit_profile/", views.UserProfileEditView.as_view(), name="edit_profile"),
    path("password/", views.PasswordChangeView.as_view(template_name="registration/change_password.html"), name="change_password"),
]
