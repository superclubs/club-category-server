# Django Rest Framework
from rest_framework import serializers

# Bases
from community.bases.api.serializers import ModelSerializer

# Models
from community.apps.communities.models import Community

# Serializers
from community.apps.posts.api.serializers import PostSerializer
from community.apps.badges.api.serializers import BadgeListSerializer


# Main Section
class CommunityListSerializer(ModelSerializer):
    master = serializers.JSONField(source='user_data')
    posts = serializers.SerializerMethodField()
    badges = serializers.SerializerMethodField()

    class Meta:
        model = Community
        fields = (
            # Main
            'id', 'master', 'banner_image_url',
            'title', 'description', 'address', 'point', 'level', 'created',
            'post_count',

            # Rank
            'live_rank', 'rising_rank', 'weekly_rank', 'monthly_rank',
            'live_rank_change', 'rising_rank_change', 'weekly_rank_change', 'monthly_rank_change',

            # Serializer
            'badges', 'posts',
        )

    def get_badges(self, obj):
        instance = obj.badges.filter(is_active=True, is_deleted=False)
        return BadgeListSerializer(instance=instance, many=True).data

    def get_posts(self, obj):
        posts = obj.posts.order_by('-created')[:3]
        return PostSerializer(instance=posts, many=True).data
