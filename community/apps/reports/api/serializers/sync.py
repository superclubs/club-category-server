from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from community.apps.reports.models import Report
from community.bases.api.serializers import ModelSerializer


class ReportSyncSerializer(ModelSerializer):
    reported_user_id = serializers.SerializerMethodField()
    club_id = serializers.SerializerMethodField()
    post_id = serializers.SerializerMethodField()
    comment_id = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = (
            "user",
            "reported_user_id",
            "title",
            "content",
            "description",
            "contents",
            "club_id",
            "post_id",
            "comment_id",
        )

    @swagger_serializer_method(serializers.IntegerField)
    def get_reported_user_id(self, obj):
        if obj.post:
            return obj.post.user.id
        elif obj.comment:
            return obj.comment.user.id
        return None

    @swagger_serializer_method(serializers.IntegerField)
    def get_community_id(self, obj):
        if obj.post:
            return obj.post.community.id
        elif obj.comment:
            return obj.comment.post.club.id
        return None

    @swagger_serializer_method(serializers.IntegerField(allow_null=True, required=False))
    def get_post_id(self, obj):
        return obj.post.id if obj.post else None

    @swagger_serializer_method(serializers.IntegerField(allow_null=True, required=False))
    def get_comment_id(self, obj):
        return obj.comment.id if obj.comment else None

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # post_id와 comment_id가 None인 경우 제거
        if representation.get("post_id") is None:
            representation.pop("post_id", None)
        if representation.get("comment_id") is None:
            representation.pop("comment_id", None)

        return representation
