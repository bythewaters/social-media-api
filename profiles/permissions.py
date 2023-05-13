from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS
from rest_framework.request import Request


class HasProfilePermission(permissions.BasePermission):
    def has_permission(self, request: Request, view: object) -> bool:
        return bool(
            request.method in SAFE_METHODS and request.user and request.user.profile
        )
