from rest_framework import serializers

from comments.models import Commentary


class CommentarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Commentary
        fields = [
            "id",
            "created_time",
            "user",
            "content",
        ]


class CommentaryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commentary
        fields = [
            "content",
        ]

    def create(self, validated_data):
        post_pk = self.context.get("post_pk")
        user = self.context.get("user")
        content = validated_data.get("content")
        comment = Commentary.objects.create(
            user=user,
            post_id=post_pk,
            content=content
        )
        comment.save()
        return comment
