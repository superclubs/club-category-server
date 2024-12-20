from community.apps.emojis.models import CommentEmoji, PostEmoji
from community.bases.api.serializers import ModelSerializer


# Main Section
class PostEmojiCreateSerializer(ModelSerializer):
    class Meta:
        model = PostEmoji
        fields = ("emoji_code",)


class CommentEmojiCreateSerializer(ModelSerializer):
    class Meta:
        model = CommentEmoji
        fields = ("emoji_code",)
