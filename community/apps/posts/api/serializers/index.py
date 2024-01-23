# DRF
from rest_framework import serializers

# Models
from community.apps.posts.models import Post

# Bases
from community.bases.api.serializers import ModelSerializer

# Serializers
from community.apps.likes.api.serializers import PostLikeSerializer


# Main Section
class PostContentSummarySerializer(ModelSerializer):
    user = serializers.JSONField(source='user_data')
    friend_status = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'thumbnail_media_url', 'user', 'title', 'content_summary', 'password', 'is_secret',
                  'public_type', 'friend_status')

    def get_friend_status(self, obj):
        request = self.context.get('request', None)
        if not request:
            return None
        user = request.user
        if not user.id:
            return None
        if obj.user == user:
            return None
        friend = obj.user.receiver_friends.filter(sender=user, is_active=True, is_deleted=False).first()
        if not friend:
            return None
        else:
            return friend.status


class PostSerializer(ModelSerializer):
    user = serializers.JSONField(source='user_data')
    medias = serializers.JSONField(source='medias_data')

    class Meta:
        model = Post
        fields = ('id', 'thumbnail_media_url', 'medias', 'user', 'title', 'comment_count', 'visit_count',
                  'total_like_count', 'like_count', 'fun_count', 'healing_count', 'legend_count', 'useful_count',
                  'empathy_count', 'devil_count', 'created')


class PostLikeResponseSerializer(ModelSerializer):
    is_liked = serializers.SerializerMethodField()
    is_disliked = serializers.SerializerMethodField()
    liked_users = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'total_like_count', 'dislike_count', 'like_count', 'fun_count', 'healing_count', 'legend_count',
                  'useful_count', 'empathy_count', 'devil_count', 'is_liked', 'is_disliked', 'liked_users')

    def get_is_liked(self, obj):
        request = self.context.get('request', None)
        if not request:
            return None
        user = request.user
        if not user.id:
            return None
        post_like = obj.post_likes.filter(user=user, is_active=True, is_deleted=False).first()
        if not post_like:
            return False
        return True

    def get_is_disliked(self, obj):
        request = self.context.get('request', None)
        if not request:
            return None
        user = request.user
        if not user.id:
            return None
        post_dislike = obj.post_dislikes.filter(user=user, is_active=True, is_deleted=False).first()
        if not post_dislike:
            return False
        return True

    def get_liked_users(self, obj):
        post_likes = obj.post_likes.filter(is_active=True, is_deleted=False)[:3]
        return PostLikeSerializer(instance=post_likes, many=True, context={'request': self.context['request']}).data
