from rest_framework import serializers

from community.apps.bookmarks.models import PostBookmark
from community.bases.api.serializers import ModelSerializer
from community.utils.bookmark_type import COMMUNITY_POST_BOOKMARK


class PostBookmarkBaseSyncSerializer(ModelSerializer):
    community_id = serializers.IntegerField(source="post.community.id")
    post_id = serializers.IntegerField(source="post.id")

    class Meta:
        model = PostBookmark
        fields = (
            "user",
            "community_id",
            "post_id",
        )


class PostBookmarkCreateSyncSerializer(PostBookmarkBaseSyncSerializer):
    username = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()

    class Meta(PostBookmarkBaseSyncSerializer.Meta):
        fields = PostBookmarkBaseSyncSerializer.Meta.fields + (
            "username",
            "type",
            "image_url",
            "content",
        )

    def get_username(self, obj):
        return obj.user.username

    def get_type(self, obj):
        return COMMUNITY_POST_BOOKMARK

    def get_image_url(self, obj):
        return obj.post.thumbnail_media_url

    def get_content(self, obj):
        return obj.post.title
