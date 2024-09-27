from django import forms
from .models import Post, Category, Tag


class PostForm(forms.ModelForm):
    # Allow input of category name as text
    category = forms.CharField(max_length=50, required=False)
    # Allow input of tags as comma-separated values
    tags = forms.CharField(
        max_length=255, required=False, help_text="Separate tags with commas"
    )

    class Meta:
        model = Post
        fields = ("title", "text", "category", "tags")

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "text": forms.Textarea(attrs={"class": "form-control"}),
            "category": forms.TextInput(attrs={"class": "form-control"}),
            "tags": forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean_category(self):
        # Retrieves the cleaned data from the category field
        #   removing any leading or trailing whitespace
        category_name = self.cleaned_data.get("category", "").strip()
        # If author of the post provides a category...
        if category_name:
            # ...fetch it from DB or create it if not exist yet...
            category, _ = Category.objects.get_or_create(name=category_name)
            return category
        return None

    def clean_tags(self):
        # Retrieves the cleaned data from the tags field
        tags_string = self.cleaned_data.get("tags", "")
        # Split it in individual tag names using "," and trims any whitespace
        tag_names = [tag.strip() for tag in tags_string.split(",") if tag.strip()]
        return tag_names

    def save(self, commit=True):
        # Save post instance first
        post = super().save(commit=False)

        if commit:
            post.save()

        # Handle tags separately (after the post is saved to get a post ID)
        tags = self.cleaned_data.get("tags")
        for tag_name in tags:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            post.tags.add(tag)

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
