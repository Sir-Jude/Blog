from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import generic

from .forms import PostForm, EditPostForm, CommentForm
from .models import Post, Category, Comment

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
    
    def get_context_data(self, *args, **kwargs):
        category_menu = Category.objects.all()
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context["category_menu"] = category_menu
        return context


def CategoryListView(request):
    category_menu_list = Category.objects.all().order_by('name')
    return render(request, 'blog/category-list.html', {'category_menu_list': category_menu_list})


def CategoryView(request, cats):
    # Adjust this line to filter correctly by category name
    category_posts = Post.objects.filter(category__name=cats.replace('-', ' '))
    
    return render(request, 'blog/categories.html', {
        'cats': cats.title().replace('-', ' '), 
        'category_posts': category_posts
    })



class DetailView(generic.DetailView):
    model = Post
    template_name = "blog/detail.html"

    def get_queryset(self):
        """
        Excludes any posts that aren't published yet.
        """
        return Post.objects.filter(pub_date__lte=timezone.now())
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_likes'] = self.object.total_likes()  # Get total likes for the current post
        return context


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
    

class NewCategoryView(generic.CreateView):
    model = Category
    template_name = "blog/new_category.html"
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy("blog:category-list")

    def form_valid(self, form):
        # Get the category name
        category_name = form.cleaned_data.get('name').strip()

        # Check if the category already exists (case insensitive)
        if Category.objects.filter(name__iexact=category_name).exists():
            messages.error(self.request, f'Category "{category_name}" already exists.')
            return self.form_invalid(form)  # Return invalid form to show the error

        return super().form_valid(form)
    
class EditPostView(generic.UpdateView):
    model = Post
    template_name = "blog/edit_post.html"
    form_class = EditPostForm

    def get_success_url(self):
        return reverse_lazy('blog:home')

    def form_valid(self, form):
        # You can perform additional actions here if needed
        return super().form_valid(form)
    

class DeletePostView(generic.DeleteView):
    model = Post
    template_name = "blog/delete_post.html"
    
    def get_success_url(self):
        return reverse_lazy("blog:home")
    
    def form_valid(self, form):
        return super().form_valid(form)


def LikeView(request, pk):
    post = get_object_or_404(Post, pk=pk)
    liked = False
    if post.likes.filter(pk=request.user.pk).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('blog:detail', args=[str(pk)]))
    

class CommentView(generic.CreateView):
    model = Comment
    template_name = "blog/post.html"
    fields = "__all__"

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])  # Get the post by its ID
        form.instance.user = self.request.user  # Set the current user as the commenter
        form.instance.post = post  # Associate the comment with the post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:detail', args=[self.kwargs['post_id']])
    
class NewCommentView(generic.CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/new_comment.html"

    def form_valid(self, form):
        # Get the post using the pk from URL parameters
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        
        # Set the current logged-in user to the comment
        form.instance.user = self.request.user
        
        # Associate the comment with the post
        form.instance.post = post

        # Proceed with the usual form saving process
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy("blog:detail", args=[self.kwargs['pk']])