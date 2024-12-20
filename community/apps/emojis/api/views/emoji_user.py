from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.openapi import TYPE_STRING, Parameter
from drf_yasg.utils import swagger_auto_schema

from community.apps.emojis.api.serializers import (
    CommentEmojiUserListSerializer,
    PostEmojiUserListSerializer,
)
from community.apps.emojis.models import CommentEmoji, PostEmoji
from community.bases.api import mixins
from community.utils.decorators import swagger_decorator
from community.bases.api.viewsets import GenericViewSet


# Main Section
class PostEmojiUsersViewSet(mixins.ListModelMixin, GenericViewSet):
    serializers = {"default": PostEmojiUserListSerializer}
    filter_backends = (DjangoFilterBackend,)

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return None
        emoji_code = self.request.query_params.get("emoji_code", None)
        queryset = PostEmoji.objects.filter_by_post_and_emoji(self.kwargs["post_pk"], emoji_code, self.request.user)
        return queryset

    @swagger_auto_schema(
        manual_parameters=[
            Parameter(name="emoji_code", in_="query", type=TYPE_STRING),
        ],
        **swagger_decorator(
            tag="03. 포스트",
            id="포스트 이모지 유저 리스트 조회",
            description="",
            response={200: PostEmojiUserListSerializer},
        )
    )
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)


class CommentEmojiUsersViewSet(mixins.ListModelMixin, GenericViewSet):
    serializers = {"default": CommentEmojiUserListSerializer}
    filter_backends = (DjangoFilterBackend,)

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return None
        emoji_code = self.request.query_params.get("emoji_code", None)
        queryset = CommentEmoji.objects.filter_by_comment_and_emoji(
            self.kwargs["comment_pk"], emoji_code, self.request.user
        )
        return queryset

    @swagger_auto_schema(
        manual_parameters=[
            Parameter(name="emoji_code", in_="query", type=TYPE_STRING),
        ],
        **swagger_decorator(
            tag="04. 댓글",
            id="댓글 이모지 유저 리스트 조회",
            description="",
            response={200: CommentEmojiUserListSerializer},
        )
    )
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)
