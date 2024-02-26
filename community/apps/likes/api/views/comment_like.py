# Django
from django_filters.rest_framework import DjangoFilterBackend

# Third Party
from drf_yasg.utils import swagger_auto_schema

# Serializers
from community.apps.likes.api.serializers import CommentLikeListSerializer

# Bases
from community.bases.api import mixins
from community.bases.api.viewsets import GenericViewSet

# Utils
from community.utils.decorators import swagger_decorator

# Models
from community.apps.likes.models import CommentLike


# Main Section
class CommentLikesViewSet(mixins.ListModelMixin,
                          GenericViewSet):
    serializers = {
        'default': CommentLikeListSerializer,
    }
    filter_backends = (DjangoFilterBackend,)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return None
        queryset = CommentLike.available.filter(comment=self.kwargs['comment_pk'], is_active=True)
        return queryset

    @swagger_auto_schema(**swagger_decorator(tag='05. 댓글',
                                             id='댓글 좋아요 리스트 조회',
                                             description='## < 댓글 좋아요 리스트 조회 API 입니다. >',
                                             response={200: CommentLikeListSerializer}
                                             ))
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)
