# Django
from django.conf import settings

# DRF
from rest_framework import serializers

# Serializers
from community.apps.post_tags.api.serializers.list import PostTagListSerializer
from community.apps.badges.api.serializers.list import BadgeListSerializer
from community.apps.comments.api.serializers.index import CommentSerializer
from community.apps.likes.api.serializers.index import PostLikeSerializer

# Models
from community.apps.posts.models.index import Post

# Bases
from community.bases.api.serializers import ModelSerializer


# Main Section
class PostSyncSerializer(ModelSerializer):
    service_type = serializers.SerializerMethodField()
    post_id = serializers.IntegerField(source='id')
    community_id = serializers.IntegerField(source='community.id')
    depth1_category_id = serializers.IntegerField(source='depth1_community_id')
    depth2_category_id = serializers.IntegerField(source='depth2_community_id')
    depth3_category_id = serializers.IntegerField(source='depth3_community_id')
    badges_data = serializers.SerializerMethodField()
    tags_data = serializers.SerializerMethodField()
    liked_users_data = serializers.SerializerMethodField()
    commented_users_data = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            # Service
            'service_type',

            # Post
            'post_id',

            # 'Community'
            'community_id', 'depth1_category_id', 'depth2_category_id', 'depth3_category_id',

            # Board Group
            'board_group_id', 'board_group_title',

            # Board
            'board_id', 'board_title',

            # User
            'user', 'user_data',

            # Profile
            'profile', 'profile_data',

            # Permission
            'read_permission',

            # Badges
            'badges_data',

            # Tags
            'tags_data',

            # Media
            'thumbnail_media_url', 'medias_data',

            # Main
            'title', 'content_summary',
            'password', 'public_type', 'reserved_at', 'boomed_at',

            # Rank
            'point', 'live_rank', 'rising_rank', 'weekly_rank', 'monthly_rank',
            'live_rank_change', 'rising_rank_change', 'weekly_rank_change', 'monthly_rank_change',

            # Count
            'comment_count', 'visit_count', 'share_count',
            'total_like_count', 'like_count', 'dislike_count',
            'fun_count', 'healing_count', 'legend_count', 'useful_count', 'empathy_count', 'devil_count',

            # Boolean
            'is_notice', 'is_event', 'is_temporary', 'is_secret',
            'is_search', 'is_share', 'is_comment', 'is_reserved', 'is_boomed',

            # Serializer
            'liked_users_data', 'commented_users_data',

            # Date
            'created', 'achieved_20_points_at',
        )

    def get_service_type(self, obj):
        return settings.SERVICE_TITLE

    def get_badges_data(self, obj):
        instance = obj.badges.order_by('id')
        return BadgeListSerializer(instance=instance, many=True).data

    def get_tags_data(self, obj):
        instance = obj.post_tags.order_by('order')
        return PostTagListSerializer(instance=instance, many=True).data

    def get_liked_users_data(self, obj):
        post_likes = obj.post_likes.filter(is_active=True, is_deleted=False)[:3]
        if post_likes:
            return PostLikeSerializer(instance=post_likes, many=True).data
        else:
            return None

    def get_commented_users_data(self, obj):
        comment = obj.comments.filter(is_active=True, is_deleted=False).order_by('-point').first()
        if comment:
            return CommentSerializer(instance=comment).data
        else:
            return None
