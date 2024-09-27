from django.contrib import admin
from .models import Post, Comment, Category, Tag

# Register your models here.


class CommentInLine(admin.TabularInline):
    model = Comment


class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Post", {"fields": ["title", "text"]}),
        ("Categorization", {"fields": ["category", "tags"]}),
        (
            "Date information",
            {"fields": ["pub_date", "last_edited"], "classes": ["collapse"]},
        ),
    ]
    list_display = ["title", "pub_date", "last_edited"]
    list_filter = ["pub_date", "last_edited"]
    search_fields = ["title"]
    readonly_fields = ("pub_date", "last_edited")


admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Tag)