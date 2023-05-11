from rest_framework import serializers
from profiles.models import Profile
from users.serializers import UserSerializer


class ProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "bio",
            "location",
            "profile_picture",
            "followers",
            "following",
        ]


class ProfileDetailSerializer(ProfileListSerializer):
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
            "followers",
            "following",
        ]


class UpdateProfileSerializer(ProfileListSerializer):
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
