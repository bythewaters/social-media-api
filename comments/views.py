from rest_framework import permissions, mixins
from rest_framework.viewsets import GenericViewSet

from comments.models import Commentary
from comments.serializers import CommentaryCreateSerializer, CommentarySerializer


class CommentaryListViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = CommentarySerializer
    queryset = Commentary.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class CommentaryCreateViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = CommentaryCreateSerializer
    queryset = Commentary.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
