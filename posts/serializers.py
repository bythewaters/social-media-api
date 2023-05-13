from rest_framework import serializers

from comments.serializers import CommentarySerializer
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    commentaries = CommentarySerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "owner",
            "title",
            "content",
            "created_time",
            "commentaries"
        ]


class PostCreateSerializer(PostSerializer):
    class Meta:
        model = Post
        fields = [
            "title",
            "content",
        ]
