from django.conf import settings
from rest_framework import serializers

from community.apps.emojis.models import PostEmoji
from community.bases.api.serializers import ModelSerializer


# Main Section
class PostEmojiSyncSerializer(ModelSerializer):
    service_type = serializers.SerializerMethodField()
    post_id = serializers.IntegerField(source="post.id")

    class Meta:
        model = PostEmoji
        fields = ("id", "user", "post_id", "emoji_code", "service_type", "created", "modified")

    def get_service_type(self, obj):
        return settings.SERVICE_TITLE


class PostEmojiDeleteSyncSerializer(PostEmojiSyncSerializer):
    class Meta(PostEmojiSyncSerializer.Meta):
        fields = (
            "service_type",
            "post_id",
            "user",
        )
