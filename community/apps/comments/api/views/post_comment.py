# Django
from django_filters.rest_framework import DjangoFilterBackend

# Django Rest Framework
from rest_framework.filters import OrderingFilter

# Third Party
from drf_yasg.utils import swagger_auto_schema

# Bases
from community.bases.api import mixins
from community.bases.api.viewsets import GenericViewSet

# Utils
from community.utils.decorators import swagger_decorator

# Serializers
from community.apps.comments.api.serializers import ParentCommentListSerializer

# Models
from community.apps.comments.models import Comment


# Main Section
class CommentsViewSet(mixins.ListModelMixin,
                      GenericViewSet):
    serializers = {
        'default': ParentCommentListSerializer
    }
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ['point', 'created']

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return None
        queryset = Comment.active.filter(post=self.kwargs['post_pk'])
        return queryset

    @swagger_auto_schema(**swagger_decorator(tag='04. 포스트',
                                             id='댓글 리스트 조회',
                                             description='## < 댓글 리스트 조회 API 입니다. >\n'
                                                         '### ordering : `point (포인트순)`, `created (생성순)` \n',
                                             response={200: ParentCommentListSerializer}
                                             ))
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)
