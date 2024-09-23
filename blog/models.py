import datetime

from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

import textwrap


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="category",
    )
    tags = models.ManyToManyField(Tag, blank=True)
    pub_date = models.DateTimeField(
        default=timezone.now, editable=False
    )  # Auto-set on creation
    last_edited = models.DateTimeField(
        null=True, blank=True
    )  # Only set when actually edited

    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    def was_published_recently(self):
        now = timezone.now().date()
        return now - datetime.timedelta(days=30) <= self.pub_date <= now

    def save(self, *args, **kwargs):
        if self.pk is not None:  # Check if the object exists (not a new post)
            original_post = Post.objects.get(pk=self.pk)
            if original_post.title != self.title or original_post.text != self.text:
                self.last_edited = timezone.now()
        else:
            self.last_edited = None

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments", null=False
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments", null=True, blank=True
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        default=timezone.now, editable=False
    )  # Auto-set on creation
    last_edited = models.DateTimeField(
        null=True, blank=True
    )  # Only set when actually edited

    def __str__(self):
        return textwrap.shorten(self.text, width=20, placeholder="...")
