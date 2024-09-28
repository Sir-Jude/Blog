from django import forms
from .models import Post, Category

choices = Category.objects.all().values_list('name', 'name')

choice_list = []

for cat in choices:
    choice_list.append(cat)

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "text", "category")

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "text": forms.Textarea(attrs={"class": "form-control"}),
            "category": forms.Select(choices=choice_list, attrs={"class": "form-control"}),
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
