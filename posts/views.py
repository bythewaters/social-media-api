from datetime import datetime
from typing import Optional

from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from django.urls import reverse
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import permissions, mixins, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import GenericViewSet

from comments.serializers import CommentaryCreateSerializer
from likes.models import Like
from likes.serializers import LikeCreateSerializer, LikeDeleteSerializer
from .models import Post
from .serializers import PostSerializer, PostCreateSerializer, PostDetailSerializer


class CreatePostView(
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer: Serializer[Post]) -> None:
        serializer.save(owner=self.request.user)


class PostListView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self) -> QuerySet[Post]:
        """Filtering posts by title and created_time"""
        queryset = self.queryset
        title = self.request.query_params.get("title")
        created_time = self.request.query_params.get("created_time")
        if title:
            return queryset.filter(title__icontains=title)
        if created_time:
            date = datetime.strptime(created_time, "%Y-%m-%d").date()
            queryset = queryset.filter(created_time__date=date)
        return queryset

    def get_serializer_class(self):
        if self.action == "add_comment":
            return CommentaryCreateSerializer
        if self.action == "retrieve":
            return PostDetailSerializer
        if self.action == "like":
            return LikeCreateSerializer
        if self.action == "dislike":
            return LikeDeleteSerializer
        return self.serializer_class

    @action(
        methods=["GET"],
        detail=False,
        url_path="my-posts",
        permission_classes=[permissions.IsAuthenticated],
    )
    def my_posts(self, request: Request) -> Response:
        """Endpoint for get all post current user"""
        posts = Post.objects.filter(owner=request.user)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=["GET"],
        detail=False,
        url_path="followers-posts",
        permission_classes=[permissions.IsAuthenticated],
    )
    def followers_posts(self, request: Request) -> Response:
        """Endpoint for get followers posts"""
        user = request.user
        followers = user.profile.followers.all()
        posts = Post.objects.filter(owner__in=followers).order_by("-created_time")
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=["POST"],
        detail=True,
        url_path="add-comment",
        permission_classes=[permissions.IsAuthenticated],
    )
    def add_comment(self, request: Request, pk: Optional[int]) -> Response:
        """Endpoint for get all post current user"""
        user = self.request.user
        serializer = self.get_serializer(
            data=request.data, context={"post_pk": pk, "user": user}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=["GET", "POST"],
        detail=True,
        url_path="like",
        permission_classes=[permissions.IsAuthenticated],
    )
    def like(self, request: Request, pk: Optional[int]) -> HttpResponseRedirect:
        """Endpoint for like post"""
        user = self.request.user
        post = Post.objects.get(pk=pk)
        if not post.likes.filter(user=user).exists():
            like = Like.objects.create(user=user, post_id=pk)
            post.likes.add(like)
        return HttpResponseRedirect(reverse("posts:post_list-list"))

    @action(
        methods=["GET", "POST"],
        detail=True,
        url_path="dislike",
        permission_classes=[permissions.IsAuthenticated],
    )
    def dislike(self, request: Request, pk: Optional[int]) -> HttpResponseRedirect:
        """Endpoint for dislike post"""
        user = self.request.user
        post = Post.objects.get(pk=pk)
        if post.likes.filter(user=user).exists():
            post.likes.get(user=user).delete()
        return HttpResponseRedirect(reverse("posts:post_list-list"))

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "title",
                type=OpenApiTypes.STR,
                description="Filter by title name (ex. ?title=something)",
            ),
            OpenApiParameter(
                "created_time",
                type=OpenApiTypes.DATE,
                description=(
                        "Filter by created_time of posts (ex. ?date=2022-10-23)"
                ),
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
