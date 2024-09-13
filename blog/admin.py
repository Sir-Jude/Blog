from django.contrib import admin
from .models import Post
from django.utils import timezone

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_date', 'last_edited')
    list_filter = ('created_date', 'last_edited')
    readonly_fields = ('created_date', 'last_edited')

admin.site.register(Post, PostAdmin)
