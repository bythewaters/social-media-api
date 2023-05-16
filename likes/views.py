from rest_framework import mixins, permissions
from rest_framework.viewsets import GenericViewSet

from likes.models import Like, Dislike
from likes.serializers import (
    LikeCreateSerializer,
    LikeSerializer,
    LikeDeleteSerializer,
    DislikeCreateSerializer,
    DislikeDeleteSerializer,
    DislikeSerializer,
)


class ReactionCreateViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = LikeCreateSerializer
    queryset = Like.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class ReactionDeleteViewSet(mixins.DestroyModelMixin, GenericViewSet):
    serializer_class = LikeDeleteSerializer
    queryset = Like.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class ReactionListViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = LikeSerializer
    queryset = Like.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class DislikeCreateViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = DislikeCreateSerializer
    queryset = Dislike.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class DislikeDeleteViewSet(mixins.DestroyModelMixin, GenericViewSet):
    serializer_class = DislikeDeleteSerializer
    queryset = Dislike.objects.all()
    permission_classes = [
        permissions.IsAuthenticated
    ]


class DislikeListViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = DislikeSerializer
    queryset = Dislike.objects.all()
    permission_classes = [
        permissions.IsAuthenticated
    ]
