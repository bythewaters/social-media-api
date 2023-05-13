from django.urls import path, include
from rest_framework import routers

from comments.views import CommentaryCreateViewSet, CommentaryListViewSet

router = routers.DefaultRouter()
router.register("create", CommentaryCreateViewSet, basename="create_comment")
router.register("list", CommentaryListViewSet, basename="comment_list")

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "comments"
