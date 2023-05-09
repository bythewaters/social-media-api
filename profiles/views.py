from django.db.models import QuerySet
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
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

    def get_queryset(self) -> QuerySet[Profile]:
        queryset = self.queryset
        username = self.request.query_params.get("username")
        location = self.request.query_params.get("location")
        if username:
            return queryset.filter(username__icontains=username)
        if location:
            return queryset.filter(location__icontains=location)
        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "username",
                type=OpenApiTypes.STR,
                description="Filter by username (ex. ?username=username_user)",
            ),
            OpenApiParameter(
                "location",
                type=OpenApiTypes.STR,
                description="Filter by location (ex. ?location=location_user)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


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

    def get_queryset(self) -> QuerySet[Profile]:
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
