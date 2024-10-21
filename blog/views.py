from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.files.storage import default_storage
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import generic

from .forms import PostForm, EditPostForm, CommentForm
from .models import Post, Category, Comment

# Create your views here.


class BaseCategoryView(generic.View):
    def get_category_menu(self):
        return Category.objects.all().order_by("name")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category_menu"] = self.get_category_menu()
        return context
    

class HomeView(BaseCategoryView, generic.ListView):
    template_name = "blog/home.html"
    context_object_name = "latest_post_list"
    ordering = ["-pub_date"]

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


def CategoryListView(request):
    category_menu_list = Category.objects.all().order_by("name")
    return render(
        request, "blog/category-list.html", {"category_menu_list": category_menu_list}
    )


class CategoryView(BaseCategoryView, generic.ListView):
    model = Post
    template_name = "blog/categories.html"
    context_object_name = "category_posts"
    
    def get_queryset(self):
        # Get the category name from the URL parameter
        cats = self.kwargs.get("cats", "").replace("-", " ")
        # Filter posts by category name
        return Post.objects.filter(category__name=cats)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cats = self.kwargs.get("cats", "").title().replace("-", " ")
        context["cats"] = cats  # Pass the category name to the context
        return context


class DetailView(BaseCategoryView, generic.DetailView):
    model = Post
    template_name = "blog/detail.html"

    def get_queryset(self):
        """
        Excludes any posts that aren't published yet.
        """
        return Post.objects.filter(pub_date__lte=timezone.now())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_likes"] = (
            self.object.total_likes()
        )  # Get total likes for the current post
        return context


class NewPostView(UserPassesTestMixin, BaseCategoryView, generic.CreateView):
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
    
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser
    

# Check if the user has admin privileges
def is_admin(user):
    return user.is_authenticated and user.is_superuser

@user_passes_test(is_admin)
def custom_upload_function(request):
    if request.method == "POST" and request.FILES.get("upload"):
        uploaded_file = request.FILES["upload"]
        
        if not uploaded_file.name.endswith(('.png', '.jpg', '.jpeg', '.gif')):
            return JsonResponse({"error": "Invalid file type"}, status=400)
        
        # Generate a name for the uploaded file
        file_name = default_storage.save(uploaded_file.name, uploaded_file)
        # Generate a URL to the uploaded file
        file_url = default_storage.url(file_name)
        # Return a JSON response with the uploaded file URL
        return JsonResponse({"url": file_url})
    
    return JsonResponse({"error": "Invalid request"}, status=400)

class NewCategoryView(UserPassesTestMixin, BaseCategoryView, generic.CreateView):
    model = Category
    template_name = "blog/new_category.html"
    fields = "__all__"

    def get_success_url(self):
        return reverse_lazy("blog:category-list")

    def form_valid(self, form):
        # Get the category name
        category_name = form.cleaned_data.get("name").strip()

        # Check if the category already exists (case insensitive)
        if Category.objects.filter(name__iexact=category_name).exists():
            messages.error(self.request, f'Category "{category_name}" already exists.')
            return self.form_invalid(form)  # Return invalid form to show the error

        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser
    

class EditPostView(UserPassesTestMixin, BaseCategoryView, generic.UpdateView):
    model = Post
    template_name = "blog/edit_post.html"
    form_class = EditPostForm

    def get_success_url(self):
        return reverse_lazy("blog:home")

    def form_valid(self, form):
        # You can perform additional actions here if needed
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser
    

class DeletePostView(UserPassesTestMixin, BaseCategoryView, generic.DeleteView):
    model = Post
    template_name = "blog/delete_post.html"

    def get_success_url(self):
        return reverse_lazy("blog:home")

    def form_valid(self, form):
        return super().form_valid(form)
    
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser


def LikeView(request, pk):
    post = get_object_or_404(Post, pk=pk)
    liked = False
    if post.likes.filter(pk=request.user.pk).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse("blog:detail", args=[str(pk)]))


class CommentView(UserPassesTestMixin,generic.CreateView):
    model = Comment
    template_name = "blog/post.html"
    fields = "__all__"

    def form_valid(self, form):
        post = get_object_or_404(
            Post, pk=self.kwargs["post_id"]
        )  # Get the post by its ID
        form.instance.user = self.request.user  # Set the current user as the commenter
        form.instance.post = post  # Associate the comment with the post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("blog:detail", args=[self.kwargs["post_id"]])
    
    def test_func(self):
        return self.request.user.is_authenticated


class NewCommentView(UserPassesTestMixin, BaseCategoryView, generic.CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/new_comment.html"

    def form_valid(self, form):
        # Get the post using the pk from URL parameters
        post = get_object_or_404(Post, pk=self.kwargs["pk"])

        # Set the current logged-in user to the comment
        form.instance.user = self.request.user

        # Associate the comment with the post
        form.instance.post = post

        # Proceed with the usual form saving process
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("blog:detail", args=[self.kwargs["pk"]])
    
    def test_func(self):
        return self.request.user.is_authenticated
