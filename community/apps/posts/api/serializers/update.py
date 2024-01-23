# DRF
from rest_framework import serializers

# Models
from community.apps.posts.models import Post
from community.apps.communities.models import Community
from community.apps.posts.models.mixins.image import get_thumbnail_media_url_and_medias_data

# Bases
from community.bases.api.serializers import ModelSerializer

# Utils
from community.utils.api.fields import HybridImageField
from community.utils.fields import extract_content_summary


# Main Section
class PostUpdateSerializer(ModelSerializer):
    tags = serializers.ListField(child=serializers.CharField(allow_blank=False), required=False)
    communities = serializers.ListField(child=serializers.PrimaryKeyRelatedField(queryset=Community.available.all()),
                                        required=False)

    class Meta:
        model = Post
        fields = ('board', 'title', 'content', 'tags', 'password', 'public_type', 'reserved_at', 'is_temporary',
                  'is_secret', 'is_notice', 'is_event', 'is_comment', 'is_share', 'is_search', 'communities')

    def update(self, instance, validated_data):
        additional_data = dict()
        tags = validated_data.pop('tags', None)

        board = validated_data.get('board', None)
        content = validated_data.get('content', None)
        reserved_at = validated_data.get('reserved_at', None)

        # Community Ids
        main_community = None
        communities = validated_data.pop('communities', None)

        if communities:
            depth_community_ids = [f'depth{i + 1}_community_id' for i, _ in enumerate(communities)]

            for i, community in enumerate(communities):
                depth_community_id = depth_community_ids[i]
                additional_data[depth_community_id] = community.id

                if i == len(communities) - 1:
                    main_community = community

            additional_data['community'] = main_community

        # Content Summary
        if content:
            content_summary = extract_content_summary(content)
            additional_data['content_summary'] = content_summary

            # Thumbnail_media_url & Medias_data
            if not instance.is_vote:
                thumbnail_media_url, medias_data = get_thumbnail_media_url_and_medias_data(content=content,
                                                                                           uuid=instance.user.uuid)

                if thumbnail_media_url is not None and medias_data is not None:
                    additional_data['medias_data'] = medias_data
                    additional_data['thumbnail_media_url'] = thumbnail_media_url

        # Update Board
        if board:
            _board_group = instance.board_group
            board_group = board.board_group
            if _board_group != board_group:
                additional_data['board_group'] = board_group
                additional_data['board_group_title'] = board_group.title

            additional_data['board_title'] = board.title
            additional_data['read_permission'] = board.read_permission

        data = dict(validated_data, **additional_data)

        if reserved_at:
            is_reserved = True
            data['is_reserved'] = is_reserved

        instance.update(**data)

        if tags:
            instance.update_post_tag(tags)

        return instance


class PostTagUpdateSerializer(ModelSerializer):
    tags = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = Post
        fields = ('tags',)


class PostThumbnailImageUpdateSerializer(ModelSerializer):
    thumbnail_media = HybridImageField(use_url=False, required=True)

    class Meta:
        model = Post
        fields = ('thumbnail_media',)
