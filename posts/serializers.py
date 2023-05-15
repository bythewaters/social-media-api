from typing import Optional

from rest_framework import serializers

from comments.serializers import CommentarySerializer
from likes.serializers import LikeSerializer, DislikeSerializer
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    comments = serializers.IntegerField(read_only=True)
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "owner",
            "title",
            "content",
            "created_time",
            "comments",
            "likes_count",
            "dislikes_count",
        ]

    @staticmethod
    def get_likes_count(instance: Post) -> Optional[int]:
        """This method count all likes"""
        return instance.likes.count()

    @staticmethod
    def get_dislikes_count(instance: Post) -> Optional[int]:
        """This method count all dislikes"""
        return instance.dislikes.count()

    def to_representation(self, instance: Post) -> dict:
        """
        Override the default to_representation method to add the comments_count
        field to the serialized output.
        """
        data = super().to_representation(instance)
        data["comments"] = instance.commentaries.count()
        return data


class PostDetailSerializer(serializers.ModelSerializer):
    commentaries = CommentarySerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)
    dislikes = DislikeSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "owner",
            "title",
            "content",
            "created_time",
            "commentaries",
            "likes",
            "dislikes"
        ]


class PostCreateSerializer(PostSerializer):
    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "created_time"
        ]
