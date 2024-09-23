from django.urls import path
from . import views

app_name = "blog"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("write/", views.IndexView.as_view(), name="write"),
    path("<int:pk>", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", views.DetailView.as_view(), name="edit"),
    path("<int:pk>/comment/", views.DetailView.as_view(), name="comment"),
]
