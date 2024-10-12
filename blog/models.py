import datetime

from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone

import textwrap


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse("blog:home")

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
        related_name="%(app_label)s_%(class)s_related",
    )
    pub_date = models.DateTimeField(
        default=timezone.now, editable=False
    )  # Auto-set on creation
    last_edited = models.DateTimeField(
        null=True, blank=True
    )  # Only set when actually edited
    likes = models.ManyToManyField(
        User,
        blank=True,
        related_name="%(app_label)s_%(class)s_related",
    )

    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    def was_published_recently(self):
        now = timezone.now().date()
        # Check if the post was published within the last 30 days.
        return now - datetime.timedelta(days=30) <= self.pub_date <= now

    def get_absolute_url(self):
        return reverse("blog:detail", args=[self.pk])

    def save(self, *args, **kwargs):
        # Check if the object exists (not a new post)
        if self.pk is not None:
            original_post = Post.objects.get(pk=self.pk)
            # Update last_edited only if title or text has changed
            if original_post.title != self.title or original_post.text != self.text:
                self.last_edited = timezone.now()
        else:
            self.last_edited = None  # For new posts, last_edited should be None

        # Ensure that last_edited is included in update_fields if it has changed,
        # otherwise it will not be updated in the DB.
        update_fields = kwargs.get("update_fields")
        if update_fields is not None and "last_edited" not in update_fields:
            update_fields = {"last_edited"}.union(update_fields)
            kwargs["update_fields"] = update_fields

        super().save(*args, **kwargs)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_related",
        null=False,
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_related",
        null=True,
        blank=True,
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        default=timezone.now, editable=False
    )  # Auto-set on creation
    last_edited = models.DateTimeField(
        null=True, blank=True
    )  # Only set when actually edited

    def save(self, *args, **kwargs):
        # Check if the object exists (not a new comment)
        if self.pk is not None:
            original_comment = Comment.objects.get(pk=self.pk)
            # Update last_edited only if the text has changed
            if original_comment.text != self.text:
                self.last_edited = timezone.now()
        else:
            self.last_edited = None  # For new comments, last_edited should be None

        # Ensure that last_edited is included in update_fields if it has changed,
        #   otherwise it will not be updated in the DB.
        update_fields = kwargs.get("update_fields")
        if update_fields is not None and "last_edited" not in update_fields:
            update_fields = {"last_edited"}.union(update_fields)
            kwargs["update_fields"] = update_fields

        super().save(*args, **kwargs)

    def __str__(self):
        return textwrap.shorten(self.text, width=20, placeholder="...")
