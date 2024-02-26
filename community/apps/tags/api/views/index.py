# Django Rest Framework
from django_filters.rest_framework import DjangoFilterBackend

# Third Party
from drf_yasg.utils import swagger_auto_schema

# Bases
from community.bases.api import mixins
from community.bases.api.viewsets import GenericViewSet

# Utils
from community.utils.decorators import swagger_decorator

# Filters
from community.apps.tags.api.views.filters import TagFilter

# Models
from community.apps.tags.models import Tag

# Serializers
from community.apps.tags.api.serializers import TagListSerializer


# Main Section
class TagsViewSet(mixins.ListModelMixin,
                  GenericViewSet):
    serializers = {
        'default': TagListSerializer,
    }
    queryset = Tag.available.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TagFilter

    @swagger_auto_schema(**swagger_decorator(tag='03. 태그',
                                             id='태그 리스트 조회',
                                             description='## < 태그 리스트 조회 API 입니다. >\n'
                                                         '### `community`: 커뮤니티 id로 필터링 \n'
                                                         '### `has_posts` : true 입력 시 필요 없는 post가 있는 태그만 필터링 \n'
                                                         '### `has_bookmark_posts` : true 입력 시 Bookmark post 태그 필터링',
                                             response={200: TagListSerializer}
                                             ))
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)
