from django.urls import path
from . import views

app_name = "blog"
urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("<int:pk>", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/comment/", views.DetailView.as_view(), name="comment"),
]
