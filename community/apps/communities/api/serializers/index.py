# Django Rest Framework
from rest_framework import serializers

# Bases
from community.bases.api.serializers import ModelSerializer

# Models
from community.apps.communities.models import Community

# Serializers
from community.apps.badges.api.serializers import BadgeListSerializer


# Main Section
class CommunitySerializer(ModelSerializer):
    master = serializers.JSONField(source='user_data')
    badges = serializers.SerializerMethodField()

    class Meta:
        model = Community
        fields = ('id', 'banner_image_url', 'badges', 'master', 'title', 'description', 'level',
                  'rising_rank', 'rank', 'live_rank', 'live_rank_change', 'rising_rank', 'rising_rank_change',
                  'post_count')

    def get_badges(self, obj):
        instance = obj.badges.filter(is_active=True, is_deleted=False).order_by('id')
        return BadgeListSerializer(instance=instance, many=True).data


class CommunityProfileImageSerializer(ModelSerializer):
    class Meta:
        model = Community
        fields = ('id',)


class CommunityBannerImageSerializer(ModelSerializer):
    class Meta:
        model = Community
        fields = ('id', 'banner_image_url')
