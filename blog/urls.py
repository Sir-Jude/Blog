from django.urls import path
from . import views

app_name = "blog"
urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("new_post/", views.NewPostView.as_view(), name="new_post"),
    path("add_category/", views.NewCategoryView.as_view(), name="add_category"),
    path("<int:pk>/edit/", views.EditPostView.as_view(), name="edit_post"),
    path("<int:pk>/delete/", views.DeletePostView.as_view(), name="delete_post"),
    path("category/<str:cats>/", views.CategoryView.as_view(), name="category"),
    path("<int:pk>/like", views.LikeView, name="like_post"),
    path("<int:pk>/new_comment/", views.NewCommentView.as_view(), name="new_comment"),
]
