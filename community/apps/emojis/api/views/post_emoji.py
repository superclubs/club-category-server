from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema

from community.apps.emojis.api.serializers import PostEmojiListSerializer
from community.apps.emojis.models import PostEmoji
from community.bases.api import mixins
from community.utils.decorators import swagger_decorator
from community.bases.api.viewsets import GenericViewSet


# Main Section
class PostEmojisViewSet(mixins.ListModelMixin, GenericViewSet):
    serializers = {"default": PostEmojiListSerializer}
    filter_backends = (DjangoFilterBackend,)

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return None
        queryset = PostEmoji.objects.group_by_emoji(self.kwargs["post_pk"])
        return queryset

    @swagger_auto_schema(
        **swagger_decorator(
            tag="03. 포스트",
            id="포스트 이모지 리스트 조회",
            description="",
            response={200: PostEmojiListSerializer},
        )
    )
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)
