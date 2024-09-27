from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic

from .forms import PostForm, EditPostForm
from .models import Post

# Create your views here.


class HomeView(generic.ListView):
    template_name = "blog/home.html"
    context_object_name = "latest_post_list"
    ordering = ['-pub_date']

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


class NewPostView(generic.CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/new_post.html"

    def get_success_url(self):
        """
        Returns the URL to redirect to after a successful form submission.

        This method uses "reverse_lazy" instead of "reverse" to defer the
        URL resolution until after the object has been created and has a#
        primary key (`pk`).

        Returns:
            str: The URL to the detail view of the created post.
        """
        return reverse_lazy("blog:detail", args=[self.object.pk])

    def form_valid(self, form):
        # You can add any extra logic here before the form is saved if needed
        return super().form_valid(form)
    

class EditPostView(generic.UpdateView):
    model = Post
    template_name = "blog/edit_post.html"
    form_class = EditPostForm
    
    def get_success_url(self):
        return reverse_lazy("blog:detail", args=[self.object.pk])
    
    def form_valid(self, form):
        return super().form_valid(form)
    

class DeletePostView(generic.DeleteView):
    model = Post
    template_name = "blog/delete_post.html"
    
    def get_success_url(self):
        return reverse_lazy("blog:home")
    
    def form_valid(self, form):
        return super().form_valid(form)
    

class CommentView(generic.DetailView):
    model = Post
    template_name = "blog/post.html"

    def write(request, post_id):
        post = get_object_or_404(Post, pk=post_id)

    def edit(request, post_id):
        post = get_object_or_404(Post, pk=post_id)
