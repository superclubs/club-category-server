# DRF
from rest_framework import serializers

# Bases
from community.bases.api.serializers import ModelSerializer

# Models
from community.apps.likes.models import PostLike, CommentLike, PostDislike, CommentDislike


# Main Section
class PostLikeListSerializer(ModelSerializer):
    user = serializers.JSONField(source='user_data')
    friend_status = serializers.SerializerMethodField()

    class Meta:
        model = PostLike
        fields = ('id', 'post', 'user', 'profile', 'type', 'is_active', 'friend_status', 'created', 'modified')

    def get_friend_status(self, obj):
        request = self.context.get('request', None)
        if not request:
            return None
        user = request.user
        if not user.id or obj.user == user:
            return None

        my_friend = user.my_friends.filter(user=obj.user, is_active=True, is_deleted=False).first()
        if my_friend:
            return 'APPROVED'

        my_friend_request = user.sender_friends.filter(receiver=obj.user, is_active=True, is_deleted=False).first()
        if my_friend_request and my_friend_request.status == 'PENDING':
            return 'PENDING'

        return None


class CommentLikeListSerializer(ModelSerializer):
    class Meta:
        model = CommentLike
        fields = ('id', 'comment', 'user', 'profile', 'type', 'is_active', 'created', 'modified')


class PostDislikeListSerializer(ModelSerializer):
    class Meta:
        model = PostDislike
        fields = ('id', 'post', 'user', 'profile', 'is_active', 'created', 'modified')


class CommentDislikeListSerializer(ModelSerializer):
    class Meta:
        model = CommentDislike
        fields = ('id', 'comment', 'user', 'profile', 'is_active', 'created', 'modified')
