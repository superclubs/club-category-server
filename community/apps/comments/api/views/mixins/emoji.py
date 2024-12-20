from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action

from community.apps.emojis.api.serializers import CommentEmojiCreateSerializer
from community.utils.decorators import swagger_decorator
from community.utils.api.response import Response


# Main Section
class CommentEmojiViewMixin:
    @swagger_auto_schema(
        **swagger_decorator(
            tag="04. 댓글",
            id="댓글 이모지 생성",
            description="",
            request=CommentEmojiCreateSerializer,
            response={201: "ok"},
        )
    )
    @action(detail=True, methods=["post"], url_path="emoji", url_name="_emoji")
    def comment_emoji(self, request, pk=None):
        comment = self.get_object()
        serializer = CommentEmojiCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment.emoji_comment(request.user, serializer.validated_data["emoji_code"])
        return Response(
            status=status.HTTP_201_CREATED,
            code=201,
            message=_("ok"),
        )

    @swagger_auto_schema(
        **swagger_decorator(
            tag="04. 댓글",
            id="댓글 이모지 취소",
            description="",
            request=CommentEmojiCreateSerializer,
            response={200: "ok"},
        )
    )
    @action(detail=True, methods=["post"], url_path="unemoji", url_name="comment_unemoji")
    def comment_unemoji(self, request, pk=None):
        comment = self.get_object()
        serializer = CommentEmojiCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment.unemoji_comment(request.user, serializer.validated_data["emoji_code"])
        return Response(
            status=status.HTTP_200_OK,
            code=200,
            message=_("ok"),
        )
