# from users.serializers import UserSerializer
from rest_framework import serializers

from profiles.models import Profile
from users.serializers import UserSerializer


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "id",
            "user",
            "username",
            "first_name",
            "last_name",
            "bio",
            "location",
            "profile_picture",
        ]


class ProfileListSerializer(ProfileSerializer):
    class Meta:
        model = Profile
        fields = [
            "username",
            "first_name",
            "last_name",
            "bio",
            "location",
            "profile_picture",
        ]


class ProfileDetailSerializer(ProfileSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Profile
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "bio",
            "location",
            "profile_picture",
        ]


class ProfileUpdateSerializer(ProfileDetailSerializer):
    class Meta:
        model = Profile
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "bio",
            "location",
            "profile_picture",
        ]
