from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action

from community.apps.emojis.api.serializers import PostEmojiCreateSerializer
from community.utils.decorators import swagger_decorator
from community.utils.api.response import Response


# Main Section
class PostEmojiViewMixin:
    @swagger_auto_schema(
        **swagger_decorator(
            tag="03. 포스트",
            id="포스트 이모지 생성",
            description="",
            request=PostEmojiCreateSerializer,
            response={201: "ok"},
        )
    )
    @action(detail=True, methods=["post"], url_path="emoji", url_name="post_emoji")
    def post_emoji(self, request, pk=None):
        post = self.get_object()
        serializer = PostEmojiCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post.emoji_post(request.user, serializer.validated_data["emoji_code"])
        return Response(
            status=status.HTTP_201_CREATED,
            code=201,
            message=_("ok"),
        )

    @swagger_auto_schema(
        **swagger_decorator(
            tag="03. 포스트",
            id="포스트 이모지 취소",
            description="",
            request=PostEmojiCreateSerializer,
            response={200: "ok"},
        )
    )
    @action(detail=True, methods=["post"], url_path="unemoji", url_name="post_unemoji")
    def post_unemoji(self, request, pk=None):
        post = self.get_object()
        serializer = PostEmojiCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post.unemoji_post(request.user, serializer.validated_data["emoji_code"])
        return Response(
            status=status.HTTP_200_OK,
            code=200,
            message=_("ok"),
        )
