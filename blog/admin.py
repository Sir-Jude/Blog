from django.contrib import admin
from .models import Post, Comment, Category

# Register your models here.


class CommentInLine(admin.TabularInline):
    model = Comment
    extra = 1
    readonly_fields = ("pub_date", "last_edited")


class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Post", {"fields": ["title", "text", "likes"]}),
        ("Categorization", {"fields": ["category"]}),
        (
            "Date information",
            {"fields": ["pub_date", "last_edited"], "classes": ["collapse"]},
        ),
    ]
    list_display = ["title", "pub_date", "last_edited"]
    list_filter = ["pub_date", "last_edited"]
    search_fields = ["title"]
    readonly_fields = ("pub_date", "last_edited")
    inlines = [CommentInLine]


admin.site.register(Category)
admin.site.register(Post, PostAdmin)
