from django.urls import path, include
from rest_framework import routers

from posts.views import CreatePostView, RetrievePostsView

router = routers.DefaultRouter()
router.register("create", CreatePostView, basename="create_post")
router.register("list", RetrievePostsView, basename="post_list")

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "posts"
