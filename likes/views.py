from rest_framework import mixins, permissions
from rest_framework.viewsets import GenericViewSet

from likes.models import Like
from likes.serializers import LikeCreateSerializer, LikeSerializer, LikeDeleteSerializer


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
