from rest_framework import viewsets, mixins, permissions, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from profiles.models import Profile
from profiles.permissions import HasProfilePermission
from profiles.serializers import (
    ProfileSerializer,
    ProfileUpdateSerializer,
    ProfileListSerializer,
)


class ProfileListViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = ProfileListSerializer
    queryset = Profile.objects.all()


class ProfileCreateViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()


class MyProfileViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = ProfileUpdateSerializer
    queryset = Profile.objects.all()
    permission_classes = [permissions.IsAuthenticated, HasProfilePermission]

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    @action(
        methods=["GET", "PATCH"],
        detail=False,
        url_path="update",
        permission_classes=[permissions.IsAuthenticated],
    )
    def update_profile(self, request: Request) -> Response:
        profile = self.request.user.profile
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
