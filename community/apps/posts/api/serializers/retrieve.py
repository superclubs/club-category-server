# Django
from django.db.models import Q
from django.utils.timezone import now

# DRF
from rest_framework import serializers

# Serializers
from community.apps.post_tags.api.serializers import PostTagListSerializer
from community.apps.posts.api.serializers import PostContentSummarySerializer
from community.apps.communities.api.serializers import CommunityListSerializer

# Models
from community.apps.posts.models import Post
from community.apps.communities.models import Community

# API
from community.bases.api.serializers import ModelSerializer


# Main Section
class PostRetrieveSerializer(ModelSerializer):
    user = serializers.JSONField(source='user_data')
    medias = serializers.JSONField(source='medias_data')
    communities = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_disliked = serializers.SerializerMethodField()
    is_reported = serializers.SerializerMethodField()
    is_friend = serializers.SerializerMethodField()
    prev_post = serializers.SerializerMethodField()
    next_post = serializers.SerializerMethodField()

    class Meta:
        model = Post

        fields = (
            # Main
            'id', 'prev_post', 'next_post', 'community', 'community_title', 'board_group', 'board_group_title',
            'board', 'board_title', 'read_permission', 'thumbnail_media_url', 'medias', 'user', 'content', 'title',
            'tags', 'password', 'point', 'public_type', 'reserved_at', 'boomed_at', 'boomed_period', 'communities',
            'created', 'modified',

            # Count
            'total_like_count', 'dislike_count',
            'like_count', 'fun_count',
            'healing_count', 'legend_count', 'useful_count', 'empathy_count', 'devil_count',
            'comment_count', 'visit_count', 'reported_count', 'share_count',

            # Boolean
            'is_active', 'is_temporary', 'is_secret', 'is_notice', 'is_event', 'is_search', 'is_share', 'is_comment',
            'is_reserved', 'is_boomed',

            # Serializer
            'is_liked', 'is_disliked', 'is_friend', 'is_bookmarked', 'is_reported'
        )

    def get_prev_post(self, obj):
        if not obj.board:
            return None
        prev_post = obj.board.posts.filter(id__lt=obj.id, is_temporary=False, is_active=True, is_deleted=False).exclude(
            (Q(is_reserved=True) & Q(reserved_at__gte=now())) |
            (Q(is_boomed=True) & Q(boomed_at__lte=now()))
        ).order_by('-id').first()

        if not prev_post:
            return None
        return PostContentSummarySerializer(instance=prev_post).data

    def get_next_post(self, obj):
        if not obj.board:
            return None
        next_post = obj.board.posts.filter(id__gt=obj.id, is_temporary=False, is_active=True, is_deleted=False).exclude(
            (Q(is_reserved=True) & Q(reserved_at__gte=now())) |
            (Q(is_boomed=True) & Q(boomed_at__lte=now()))
        ).order_by('id').first()

        if not next_post:
            return None
        return PostContentSummarySerializer(instance=next_post).data

    def get_tags(self, obj):
        instance = obj.post_tags.order_by('order')
        return PostTagListSerializer(instance=instance, many=True).data

    def get_communities(self, obj):
        community_ids = []

        if obj.depth1_community_id is not None:
            community_ids.append(obj.depth1_community_id)

        if obj.depth2_community_id is not None:
            community_ids.append(obj.depth2_community_id)

        if obj.depth3_community_id is not None:
            community_ids.append(obj.depth3_community_id)

        instance = Community.available.filter(id__in=community_ids)

        return CommunityListSerializer(instance=instance, many=True).data

    def get_is_bookmarked(self, obj):
        request = self.context.get('request', None)
        if not request:
            return None
        user = request.user
        if not user.id:
            return None
        post_bookmark = obj.post_bookmarks.filter(user=user, is_active=True, is_deleted=False).first()
        if not post_bookmark:
            return False
        return True

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

    def get_is_reported(self, obj):
        request = self.context.get('request', None)
        if not request:
            return None
        user = request.user
        if not user.id:
            return None
        post_report = obj.reports.filter(user=user, is_active=True, is_deleted=False).first()
        if not post_report:
            return False
        return True

    def get_is_friend(self, obj):
        request = self.context.get('request', None)
        if not request:
            return None
        user = request.user
        if not user.id:
            return None
        if user == obj.user:
            return True

        other = user.my_friends.filter(user=obj.user, is_active=True, is_deleted=False).first()

        if not other:
            return False
        return True
