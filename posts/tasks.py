from datetime import datetime

from celery import shared_task
from django.contrib.auth import get_user_model

from posts.models import Post


@shared_task
def create_post_on_a_specific_date(
    title: str, content: str, owner_id: int, eta: str
) -> None:
    """
    Task to create a post on a specific date and time.
    """
    owner = get_user_model().objects.get(id=owner_id)
    scheduled_time = datetime.strptime(eta, "%Y-%m-%dT%H:%M:%S")
    delay = (scheduled_time - datetime.now()).total_seconds()
    create_post.apply_async(args=[title, content, owner.id], countdown=delay)


@shared_task
def create_post(title: str, content: str, owner_id: str) -> None:
    """
    Task to create a post.
    """
    owner = get_user_model().objects.get(id=owner_id)
    Post.objects.create(title=title, content=content, owner=owner)
