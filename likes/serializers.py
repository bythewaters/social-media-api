from rest_framework import serializers
from likes.models import Like
from users.serializers import UserUsernameSerializer


class LikeSerializer(serializers.ModelSerializer):
    user = UserUsernameSerializer(read_only=True)

    class Meta:
        model = Like
        fields = [
            "id",
            "user",
        ]


class LikeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = [
            "user",
            "post",
        ]


class LikeDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = [
            "user",
            "post",
        ]
