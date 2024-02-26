# Django Rest Framework
from rest_framework import serializers

# Bases
from community.bases.api.serializers import ModelSerializer

# Models
from community.apps.communities.models import Community

# Serializers
from community.apps.badges.api.serializers import BadgeListSerializer


# Main Section
class CommunityRetrieveSerializer(ModelSerializer):
    master = serializers.JSONField(source='user_data')
    board_groups = serializers.JSONField(source='board_data')
    badges = serializers.SerializerMethodField()

    class Meta:
        model = Community
        fields = (
            # Main
            'id', 'banner_image_url', 'master', 'title', 'address', 'description', 'point',
            'level', 'live_rank', 'live_rank_change', 'rising_rank', 'rising_rank_change', 'board_groups', 'created',

            # Count
            'post_count', 'comment_count',

            # Serializer
            'badges'
        )

    def get_badges(self, obj):
        instance = obj.badges.filter(is_active=True, is_deleted=False).order_by('id')
        return BadgeListSerializer(instance=instance, many=True).data
