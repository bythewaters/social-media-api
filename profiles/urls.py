from django.urls import path, include
from rest_framework import routers

from profiles.views import ProfileListViewSet, MyProfileViewSet, ProfileCreateViewSet

router = routers.DefaultRouter()
router.register("", ProfileListViewSet)
router.register("me", MyProfileViewSet)
router.register("create", ProfileCreateViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "profiles"
