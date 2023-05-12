from datetime import datetime

from django.db.models import QuerySet
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import permissions, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Post
from .serializers import PostSerializer, PostCreateSerializer


class CreatePostView(
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class RetrievePostsView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self) -> QuerySet[Post]:
        queryset = self.queryset
        title = self.request.query_params.get("title")
        created_time = self.request.query_params.get("created_time")
        if title:
            return queryset.filter(title__icontains=title)
        if created_time:
            date = datetime.strptime(created_time, "%Y-%m-%d").date()
            queryset = queryset.filter(created_time__date=date)
        return queryset

    @action(
        methods=["GET"],
        detail=False,
        url_path="my-posts",
        permission_classes=[permissions.IsAuthenticated],
    )
    def my_posts(self, request):
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
    def followers_posts(self, request):
        """Endpoint for get followers posts"""
        user = request.user
        followers = user.profile.followers.all()
        posts = Post.objects.filter(owner__in=followers).order_by(
            "-created_time"
        )
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
                        "Filter by created_time of posts "
                        "(ex. ?date=2022-10-23)"
                ),
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
