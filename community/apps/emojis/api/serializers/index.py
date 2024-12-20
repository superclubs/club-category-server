from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from community.apps.emojis.models import CommentEmoji, PostEmoji
from community.apps.users.api.serializers import UsernameSerializer
from community.bases.api.serializers import ModelSerializer


# Main Section
class PostEmojiSerializer(ModelSerializer):
    count = serializers.IntegerField()
    is_selected = serializers.BooleanField()
    users = serializers.SerializerMethodField()

    class Meta:
        model = PostEmoji
        fields = (
            "emoji_code",
            "count",
            "is_selected",
            "users",
        )

    @swagger_serializer_method(UsernameSerializer(many=True))
    def get_users(self, obj):
        return UsernameSerializer(obj["users"], many=True).data


class CommentEmojiSerializer(PostEmojiSerializer):
    class Meta:
        model = CommentEmoji
        fields = PostEmojiSerializer.Meta.fields
