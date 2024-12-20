from rest_framework import serializers

from community.apps.emojis.models import CommentEmoji, PostEmoji
from community.bases.api.serializers import ModelSerializer
from community.modules.choices import FRIEND_REQUEST_AVAILABLE_STATUS


# Main Section
class PostEmojiListSerializer(ModelSerializer):
    count = serializers.IntegerField()

    class Meta:
        model = PostEmoji
        fields = (
            "emoji_code",
            "count",
        )


class PostEmojiUserListSerializer(ModelSerializer):
    id = serializers.IntegerField(source="user.id")
    username = serializers.CharField(source="user.username")
    profile_image_url = serializers.CharField(source="user.profile_image_url")
    friend_request_status = serializers.ChoiceField(
        default=None, choices=FRIEND_REQUEST_AVAILABLE_STATUS, read_only=True
    )
    friend_request_id = serializers.IntegerField(default=None, read_only=True)

    class Meta:
        model = PostEmoji
        fields = ("emoji_code", "id", "username", "profile_image_url", "friend_request_status", "friend_request_id")


class CommentEmojiListSerializer(PostEmojiListSerializer):
    class Meta:
        model = CommentEmoji
        fields = PostEmojiListSerializer.Meta.fields


class CommentEmojiUserListSerializer(PostEmojiUserListSerializer):
    class Meta:
        model = CommentEmoji
        fields = PostEmojiUserListSerializer.Meta.fields
