from rest_framework import serializers
from profiles.models import Profile
from users.serializers import UserSerializer


class ProfileListSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()

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

    @staticmethod
    def get_followers(obj: Profile) -> int:
        return obj.followers.count()

    @staticmethod
    def get_following(obj: Profile) -> int:
        return obj.following.count()


class ProfileDetailSerializer(ProfileListSerializer):
    user = UserSerializer(many=False, read_only=True)
    following = serializers.SlugRelatedField(
        slug_field="email", read_only=True, many=True
    )
    followers = serializers.SlugRelatedField(
        slug_field="email", read_only=True, many=True
    )

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
            "profile_picture",
        ]


class ProfileUploadImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "id",
            "profile_picture"
        ]
