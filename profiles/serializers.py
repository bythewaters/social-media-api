from rest_framework import serializers
from profiles.models import Profile
from users.serializers import UserSerializer


class ProfileListSerializer(serializers.ModelSerializer):
    following = serializers.SlugRelatedField(
        slug_field="email", read_only=True, many=True
    )
    followers = serializers.SlugRelatedField(
        slug_field="email", read_only=True, many=True
    )

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


class ProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "username",
            "first_name",
            "last_name",
            "bio",
            "location",
        ]


class ProfileUploadImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "id",
            "profile_picture"
        ]
