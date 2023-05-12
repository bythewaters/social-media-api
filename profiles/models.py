import os
import uuid

from django.db import models
from django.utils.text import slugify

from social_media_api import settings


def profile_image_file_path(instance: "Profile", filename: str) -> str:
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.username)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/profile/", filename)


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    username = models.CharField(max_length=100, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    bio = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to=profile_image_file_path, null=True, blank=True
    )
    followers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="follower",
        blank=True,
    )
    following = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="following",
        blank=True,
    )

    def __str__(self) -> str:
        return self.username
