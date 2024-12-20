# DRF
from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

# Models
from community.apps.comments.models import Comment
from community.apps.emojis.api.serializers import CommentEmojiSerializer
from community.apps.users.api.serializers import UserSerializer

# Serializers
from community.bases.api.serializers import ModelSerializer


# Main Section
class CommentListSerializer(ModelSerializer):
    user = UserSerializer()
    is_liked = serializers.SerializerMethodField()
    is_disliked = serializers.SerializerMethodField()
    is_reported = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    emojis = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            # Main
            "parent_comment",
            "id",
            "community",
            "post",
            "user",
            "image_url",
            "content",
            "point",
            "created",
            "modified",
            # Boolean
            "is_deleted",
            "is_secret",
            # Count
            "emoji_count",
            "total_like_count",
            "dislike_count",
            "like_count",
            "fun_count",
            "healing_count",
            "legend_count",
            "useful_count",
            "empathy_count",
            "devil_count",
            "reported_count",
            # Serializer
            "is_liked",
            "is_disliked",
            "is_reported",
            "comment_count",
            "emojis",
        )

    def get_comment_count(self, obj):
        if hasattr(obj, "child_comments"):
            return len([c for c in obj.child_comments if c.is_active and not c.is_deleted])
        return obj.comments.filter(is_active=True, is_deleted=False).count()

    def get_is_liked(self, obj):
        request = self.context.get("request", None)
        if not request:
            return None
        user = request.user
        if not user.id:
            return None

        if hasattr(obj, "is_liked"):
            return obj.is_liked

        comment_like = obj.comment_likes.filter(user=user, is_active=True).first()
        if not comment_like:
            return False
        return True

    def get_is_disliked(self, obj):
        request = self.context.get("request", None)
        if not request:
            return None
        user = request.user
        if not user.id:
            return None

        if hasattr(obj, "is_disliked"):
            return obj.is_disliked

        comment_dislike = obj.comment_dislikes.filter(user=user, is_active=True).first()
        if not comment_dislike:
            return False
        return True

    def get_is_reported(self, obj):
        request = self.context.get("request", None)
        if not request:
            return None
        user = request.user
        if not user.id:
            return None

        if hasattr(obj, "is_reported"):
            return obj.is_reported

        comment_report = obj.reports.filter(user=user, is_active=True).first()
        if not comment_report:
            return False
        return True

    @swagger_serializer_method(CommentEmojiSerializer(many=True))
    def get_emojis(self, obj):
        if not hasattr(obj, "prefetched_comment_emojis"):
            return []

        emojis = obj.prefetched_comment_emojis

        grouped_emojis = {}
        for emoji in emojis:
            emoji_code = emoji.emoji_code
            if emoji_code not in grouped_emojis:
                grouped_emojis[emoji_code] = {
                    "emoji_code": emoji_code,
                    "is_selected": emoji.is_selected,
                    "count": emoji.count,
                    "users": [],
                }

            if len(grouped_emojis[emoji_code]["users"]) < 5:
                grouped_emojis[emoji_code]["users"].append(emoji.user)

        return CommentEmojiSerializer(grouped_emojis.values(), many=True).data


class ChildCommentListSerializer(CommentListSerializer):
    class Meta:
        model = Comment
        fields = CommentListSerializer.Meta.fields


class ParentCommentListSerializer(CommentListSerializer):
    child_comments = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = CommentListSerializer.Meta.fields + ("child_comments",)

    def get_child_comments(self, obj):
        if hasattr(obj, "child_comments"):
            return ChildCommentListSerializer(
                obj.child_comments, many=True, context={"request": self.context["request"]}
            ).data

        return ChildCommentListSerializer(
            obj.comments.filter(is_active=True), many=True, context={"request": self.context["request"]}
        ).data
