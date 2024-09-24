from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Category, Tag, Post, Comment

# Create your views here.


class HomeView(generic.ListView):
    template_name = "blog/home.html"
    context_object_name = "latest_post_list"

    def get_queryset(self):
        """
        Return the last five published posts
        (not including those set to be
        published in the future).
        "__lte" = "less than or equal to"
        """
        return Post.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[
            :5
        ]


class DetailView(generic.DetailView):
    model = Post
    template_name = "blog/detail.html"

    def get_queryset(self):
        """
        Excludes any posts that aren't published yet.
        """
        return Post.objects.filter(pub_date__lte=timezone.now())


class CommentView(generic.DetailView):
    model = Post
    template_name = "blog/post.html"

    def write(request, post_id):
        post = get_object_or_404(Post, pk=post_id)
    
    def edit (request, post_id):
        post = get_object_or_404(Post, pk=post_id)
