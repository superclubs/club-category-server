from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema

from community.apps.emojis.api.serializers import CommentEmojiListSerializer
from community.apps.emojis.models import CommentEmoji
from community.bases.api import mixins
from community.utils.decorators import swagger_decorator
from community.bases.api.viewsets import GenericViewSet


# Main Section
class CommentEmojisViewSet(mixins.ListModelMixin, GenericViewSet):
    serializers = {"default": CommentEmojiListSerializer}
    filter_backends = (DjangoFilterBackend,)

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return None
        queryset = CommentEmoji.objects.group_by_emoji(self.kwargs["comment_pk"])
        return queryset

    @swagger_auto_schema(
        **swagger_decorator(
            tag="04. 댓글",
            id="댓글 이모지 리스트 조회",
            description="",
            response={200: CommentEmojiListSerializer},
        )
    )
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)
