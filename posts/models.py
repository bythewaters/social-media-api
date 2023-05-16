from django.db import models
from social_media_api import settings
from django.utils import timezone


class Post(models.Model):
    title = models.CharField(max_length=63)
    content = models.TextField()
    created_time = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="post"
    )

    def __str__(self) -> str:
        return f"{self.title}"
