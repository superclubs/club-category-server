# Python
from datetime import timedelta, datetime

# Django
from django.core.exceptions import ValidationError
from django.utils.timezone import now

# DRF
from rest_framework import serializers

# Bases
from community.bases.api.serializers import ModelSerializer

# Models
from community.apps.posts.models import Post
from community.apps.communities.models import Community
from community.apps.boards.models import Board


# Main Section
class PostCreateSerializer(ModelSerializer):
    tags = serializers.ListField(child=serializers.CharField(allow_blank=True), required=False)
    communities = serializers.ListField(child=serializers.PrimaryKeyRelatedField(queryset=Community.available.all()),
                                        required=True)

    class Meta:
        model = Post
        fields = ('board', 'title', 'content', 'public_type', 'is_secret', 'password', 'reserved_at',
                  'boomed_period', 'is_temporary', 'is_notice', 'is_event', 'is_search', 'is_share', 'is_comment',
                  'tags', 'communities')

    def create(self, validated_data):
        additional_data = dict()

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

        # FK
        user = self.context['user']
        board = validated_data.get('board', None)

        if board:
            if not Board.available.filter(id=board.id).exists():
                raise ValidationError('보드를 찾을 수 없습니다.')
        else:
            raise ValidationError('보드를 찾을 수 없습니다.')

        additional_data['community'] = main_community
        additional_data['user'] = user

        # Main Fields
        reserved_at = validated_data.get('reserved_at', None)
        boomed_period = validated_data.get('boomed_period', None)

        if reserved_at:
            if now() > reserved_at:
                raise ValidationError('과거로 예약할 수 없습니다.')

            additional_data['is_reserved'] = True

        if boomed_period:
            if reserved_at:
                boomed_at = datetime.fromisoformat(reserved_at) + timedelta(minutes=int(boomed_period))
            else:
                boomed_at = now() + timedelta(minutes=int(boomed_period))

            additional_data['boomed_at'] = boomed_at
            additional_data['is_boomed'] = True

        # Many to Many
        tags = validated_data.pop('tags', None)

        # Create Post
        data = dict(validated_data, **additional_data)
        instance = Post(**data)
        instance.save()

        # Create Tags
        if tags:
            for index, tag in enumerate(tags):
                if tag == "":
                    pass
                else:
                    instance.create_post_tag(index=index, tag=tag)

        return instance
