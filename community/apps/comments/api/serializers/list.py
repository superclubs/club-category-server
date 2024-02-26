# Django Rest Framework
from rest_framework import serializers

# Serializers
from community.bases.api.serializers import ModelSerializer

# Models
from community.apps.comments.models import Comment


# Main Section
class CommentListSerializer(ModelSerializer):
    user = serializers.JSONField(source='user_data')
    is_liked = serializers.SerializerMethodField()
    is_disliked = serializers.SerializerMethodField()
    is_reported = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            # Main
            'parent_comment', 'id', 'community', 'post', 'user', 'image_url', 'content', 'point', 'created', 'modified',

            # Boolean
            'is_deleted', 'is_secret',

            # Count
            'total_like_count', 'dislike_count', 'like_count', 'fun_count', 'healing_count', 'legend_count',
            'useful_count', 'empathy_count', 'devil_count', 'reported_count',

            # Serializer
            'is_liked', 'is_disliked', 'is_reported', 'comment_count',
        )

    def get_comment_count(self, obj):
        return obj.post.comments.filter(is_active=True, is_deleted=False).count()

    def get_is_liked(self, obj):
        request = self.context.get('request', None)
        if not request:
            return None
        user = request.user
        if not user.id:
            return None
        comment_like = obj.comment_likes.filter(user=user, is_active=True, is_deleted=False).first()
        if not comment_like:
            return False
        return True

    def get_is_disliked(self, obj):
        request = self.context.get('request', None)
        if not request:
            return None
        user = request.user
        if not user.id:
            return None
        comment_dislike = obj.comment_dislikes.filter(user=user, is_active=True, is_deleted=False).first()
        if not comment_dislike:
            return False
        return True

    def get_is_reported(self, obj):
        request = self.context.get('request', None)
        if not request:
            return None
        user = request.user
        if not user.id:
            return None
        comment_report = obj.reports.filter(user=user, is_active=True, is_deleted=False).first()
        if not comment_report:
            return False
        return True


class ChildCommentListSerializer(CommentListSerializer):
    class Meta:
        model = Comment
        fields = CommentListSerializer.Meta.fields


class ParentCommentListSerializer(CommentListSerializer):
    child_comments = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = CommentListSerializer.Meta.fields + ('child_comments',)

    def get_child_comments(self, obj):
        return ChildCommentListSerializer(obj.comments, many=True, context={'request': self.context['request']}).data
