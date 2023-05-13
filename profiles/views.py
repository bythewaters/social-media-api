from typing import Optional

from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, mixins, permissions, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.reverse import reverse

from profiles.models import Profile
from profiles.permissions import HasProfilePermission
from profiles.serializers import (
    ProfileListSerializer,
    ProfileDetailSerializer,
    UpdateProfileSerializer,
    ProfileCreateSerializer,
    ProfileUploadImageSerializer,
)


class ProfileListViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = ProfileListSerializer
    queryset = Profile.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self) -> QuerySet[Profile]:
        """Filtering by username and location"""
        queryset = self.queryset
        username = self.request.query_params.get("username")
        location = self.request.query_params.get("location")
        if username:
            return queryset.filter(username__icontains=username)
        if location:
            return queryset.filter(location__icontains=location)
        return queryset.exclude(user=self.request.user)

    def get_serializer_class(self):
        """Return serializer depend on method"""
        if self.action == "retrieve":
            return ProfileDetailSerializer
        return self.serializer_class

    @action(
        methods=["GET", "PATCH"],
        detail=True,
        url_path="unfollow",
        permission_classes=[permissions.IsAuthenticated],
    )
    def unfollow(self, request: Request, pk: Optional[int]) -> HttpResponseRedirect:
        """Endpoint for unfollow user"""
        profile = self.request.user.profile
        unfollow_user_profile = Profile.objects.get(pk=pk)
        profile.following.remove(unfollow_user_profile.user.id)
        unfollow_user_profile.followers.remove(self.request.user)
        redirect_url = reverse("profiles:profiles_list-list")
        return HttpResponseRedirect(redirect_url)

    @action(
        methods=["GET", "PATCH"],
        detail=True,
        url_path="follow",
        permission_classes=[permissions.IsAuthenticated],
    )
    def follow(self, request: Request, pk: Optional[int]) -> HttpResponseRedirect:
        """Endpoint for follow user"""
        profile = self.request.user.profile
        follow_user_profile = Profile.objects.get(pk=pk)
        profile.following.add(follow_user_profile.user.id)
        follow_user_profile.followers.add(self.request.user)
        redirect_url = reverse("profiles:profiles_list-list")
        return HttpResponseRedirect(redirect_url)

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
    serializer_class = ProfileCreateSerializer
    queryset = Profile.objects.all()
    permission_classes = [
        HasProfilePermission,
    ]


class MyProfileViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = ProfileDetailSerializer
    queryset = Profile.objects.all()
    permission_classes = [permissions.IsAuthenticated, HasProfilePermission]

    def get_queryset(self) -> QuerySet[Profile]:
        """Return queryset for current user"""
        return Profile.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        """Return serializer depend on method"""
        if self.action == "update_profile":
            return UpdateProfileSerializer
        if self.action == "upload_image":
            return ProfileUploadImageSerializer
        return self.serializer_class

    @action(
        methods=["GET", "PATCH"],
        detail=False,
        url_path="update",
        permission_classes=[permissions.IsAuthenticated],
    )
    def update_profile(self, request: Request) -> Response:
        """Endpoint for update user profile"""
        profile = self.request.user.profile
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=["POST"],
        detail=False,
        url_path="upload-image",
        permission_classes=[permissions.IsAuthenticated],
    )
    def upload_image(self, request):
        """Endpoint for uploading image to specific profile"""
        profile = self.request.user.profile
        serializer = self.get_serializer(profile, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
