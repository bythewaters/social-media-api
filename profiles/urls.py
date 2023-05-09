from django.urls import path, include
from rest_framework import routers

from profiles.views import ProfileListViewSet, MyProfileViewSet

router = routers.DefaultRouter()
router.register("", ProfileListViewSet)
router.register("me", MyProfileViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "profiles"
