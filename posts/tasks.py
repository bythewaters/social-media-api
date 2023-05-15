from celery import shared_task

from posts.models import Post
from social_media_api import settings


@shared_task
def create_post_on_a_specific_date(title, content, owner_id, eta):
    """
    The function create post on a
    specific date.
    """
    owner = settings.AUTH_USER_MODEL.objects.get(id=owner_id)
    Post.objects.create(title=title, content=content, owner=owner)
