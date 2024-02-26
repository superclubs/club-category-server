# Django Rest Framework
from rest_framework import serializers

# Serializers
from community.apps.reports.api.serializers.index import ReportSerializer

# Bases
from community.bases.api.serializers import ModelSerializer

# Models
from community.apps.reports.models import ReportChoice, ReportGroup


# Main Section
class ReportChoiceListSerializer(ModelSerializer):
    user = serializers.JSONField(source='user_data')

    class Meta:
        model = ReportChoice
        fields = ('id', 'community', 'user', 'title', 'content', 'is_default', 'is_active', 'created', 'modified')


class ReportGroupListSerializer(ModelSerializer):
    reporters = serializers.SerializerMethodField()

    class Meta:
        model = ReportGroup
        fields = ('id', 'community', 'post', 'comment', 'contents', 'reported_count', 'reporters',
                  'profile', 'username', 'is_staff', 'profile_is_banned', 'profile_is_deactivated',
                  'is_deactivated', 'deactivated_at')

    def get_reporters(self, obj):
        reports = obj.reports.filter(is_active=True, is_deleted=False).order_by('-created')[:3]
        return ReportSerializer(instance=reports, many=True).data
