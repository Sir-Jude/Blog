from django.db import models
from django.utils import timezone

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now, editable=False)  # Auto-set on creation
    last_edited = models.DateTimeField(null=True, blank=True)  # Only set when actually edited

    def save(self, *args, **kwargs):
        if self.pk is not None: # Check if the object exists (not a new post)
            original_post = Post.objects.get(pk=self.pk)
            if original_post.title != self.title or original_post.text != self.text:
                self.last_edited = timezone.now()
        else:
            self.last_edited = None
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title