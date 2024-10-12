from django import forms
from .models import Post, Category, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "text", "category")

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "text": forms.Textarea(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
        }

    def clean_category(self):
        # Retrieves the cleaned data from the category field
        category_name = self.cleaned_data.get("category", "")
        # If author of the post provides a category...
        if category_name:
            # ...fetch it from DB or create it if not exist yet...
            category, _ = Category.objects.get_or_create(name=category_name)
            return category
        return None

    def save(self, commit=True):
        # Save post instance first
        post = super().save(commit=False)

        if commit:
            post.save()

        return post


class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "text")

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "text": forms.Textarea(attrs={"class": "form-control"}),
        }

    def save(self, commit=True):
        # Save post instance first
        post = super().save(commit=False)

        if commit:
            post.save()


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("text",)

        widgets = {
            "text": forms.Textarea(attrs={"class": "form-control"}),
        }

    def save(self, commit=True):
        # Save post instance first
        comment = super().save(commit=False)

        if commit:
            comment.save()

        return comment
