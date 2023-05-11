from django.urls import path, include
from rest_framework import routers

from profiles.views import ProfileListViewSet, MyProfileViewSet, ProfileCreateViewSet

router = routers.DefaultRouter()
router.register("list", ProfileListViewSet, basename="profiles_list")
router.register("me", MyProfileViewSet, basename="my_profile")
router.register("create", ProfileCreateViewSet, basename="create_profile")

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "profiles"
