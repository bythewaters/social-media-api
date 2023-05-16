from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS
from rest_framework.request import Request

from profiles.models import Profile


class CreateProfilePermission(permissions.BasePermission):
    def has_permission(self, request: Request, view) -> bool:
        return bool(
            not Profile.objects.filter(user=request.user).exists()
        )


class HasProfilePermission(permissions.BasePermission):
    def has_permission(self, request: Request, view) -> bool:
        return bool(
            Profile.objects.filter(user=request.user).exists()
        )


class CannotSubscribeYourselfPermission(permissions.BasePermission):
    def has_permission(self, request: Request, view) -> bool:
        return bool(
            request.method in SAFE_METHODS
            and request.user != view.get_object().user
        )
