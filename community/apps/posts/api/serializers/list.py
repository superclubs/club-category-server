# Django
from django.db.models import Prefetch

# Django Rest Framework
from rest_framework import serializers

# Serializers
from community.apps.post_tags.api.serializers import PostTagListSerializer
from community.apps.badges.api.serializers import BadgeListSerializer
from community.apps.comments.api.serializers import CommentSerializer
from community.apps.likes.api.serializers import PostLikeSerializer

# Models
from community.apps.posts.models import Post
from community.apps.likes.models import PostLike, PostDislike
from community.apps.comments.models import Comment
from community.apps.badges.models import Badge
from community.apps.post_tags.models import PostTag
from community.apps.bookmarks.models import PostBookmark

# Bases
from community.bases.api.serializers import ModelSerializer


# Main Section
class PostListSerializer(ModelSerializer):
    user = serializers.JSONField(source='user_data')
    profile = serializers.JSONField(source='profile_data')
    medias = serializers.JSONField(source='medias_data')
    tags = serializers.SerializerMethodField()
    badges = serializers.SerializerMethodField()

    is_bookmarked = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_disliked = serializers.SerializerMethodField()
    is_friend = serializers.SerializerMethodField()
    is_kept = serializers.SerializerMethodField()

    liked_users = serializers.SerializerMethodField()
    commented_users = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            # Main
            'id', 'thumbnail_media_url', 'medias', 'badges',
            'community', 'community_title', 'board', 'board_title', 'read_permission',
            'user', 'profile', 'title', 'content_summary', 'tags', 'password',
            'rising_rank_change', 'public_type', 'reserved_at', 'boomed_at',
            'created', 'modified',

            # Rank
            'live_rank', 'rising_rank', 'weekly_rank', 'monthly_rank',
            'live_rank_change', 'rising_rank_change', 'weekly_rank_change', 'monthly_rank_change',

            # Count
            'point', 'comment_count', 'visit_count', 'share_count',
            'total_like_count', 'dislike_count', 'like_count', 'fun_count', 'healing_count',
            'legend_count', 'useful_count', 'empathy_count', 'devil_count',

            # Boolean
            'is_active', 'is_notice', 'is_event', 'is_temporary', 'is_secret',
            'is_search', 'is_share', 'is_comment', 'is_reserved', 'is_boomed',
            'is_agenda',

            # Serializer
            'is_bookmarked', 'is_liked', 'is_disliked', 'liked_users', 'is_friend', 'is_kept', 'commented_users'
        )

    def prefetch_related(self, queryset, user):
        queryset = queryset.prefetch_related(
            Prefetch('user'),
            Prefetch('post_likes', queryset=PostLike.available.all(), to_attr='active_likes'),
            Prefetch('comments', queryset=Comment.available.all().order_by('-point')),
            Prefetch('badges', queryset=Badge.available.all().order_by('id')),
            Prefetch('post_tags', queryset=PostTag.available.all().order_by('id')),
        )
        if user and user.id:
            queryset = queryset.prefetch_related(
                Prefetch('post_bookmarks', queryset=PostBookmark.available.filter(user=user)),
                Prefetch('post_likes', queryset=PostLike.available.filter(user=user),
                         to_attr='user_active_likes'),
                Prefetch('post_dislikes', queryset=PostDislike.available.filter(user=user))
            )
        return queryset

    def get_is_kept(self, obj):
        request = self.context.get('request', None)
        if not request:
            return None
        user = request.user
        if not user.id:
            return None
        if user == obj.user and obj.public_type == 'ONLY_ME':
            return True
        return False

    def get_is_friend(self, obj):
        request = self.context.get('request', None)
        if not request:
            return None
        user = request.user
        if not user.id:
            return None
        if user == obj.user:
            return True

        other = user.my_friends.filter(user=obj.user, is_active=True).first()

        if not other:
            return False
        return True

    def get_liked_users(self, obj):
        if hasattr(obj, 'active_likes'):
            post_likes = obj.active_likes[:3]
            return PostLikeSerializer(instance=post_likes, many=True, context={'request': self.context['request']}).data

    def get_commented_users(self, obj):
        comment = obj.comments.filter(is_active=True, is_deleted=False).first()
        return CommentSerializer(instance=comment, context={'request': self.context['request']}).data

    def get_badges(self, obj):
        instance = obj.badges.filter(is_active=True, is_deleted=False)
        return BadgeListSerializer(instance=instance, many=True).data

    def get_tags(self, obj):
        instance = obj.post_tags.filter(is_active=True, is_deleted=False)
        return PostTagListSerializer(instance=instance, many=True).data

    def get_is_bookmarked(self, obj):
        request = self.context.get('request', None)
        if not request:
            return None
        user = request.user
        if not user.id:
            return None
        post_bookmark = obj.post_bookmarks.first()
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
        if hasattr(obj, 'user_active_likes'):
            post_like = obj.user_active_likes[:1]
            if not post_like:
                return False
            return True
        return None

    def get_is_disliked(self, obj):
        request = self.context.get('request', None)
        if not request:
            return None
        user = request.user
        if not user.id:
            return None
        post_dislike = obj.post_dislikes.first()
        if not post_dislike:
            return False
        return True
