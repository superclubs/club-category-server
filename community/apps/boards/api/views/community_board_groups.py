# Django
from django_filters.rest_framework import DjangoFilterBackend

# Third Party
from drf_yasg.utils import swagger_auto_schema

# Bases
from community.bases.api import mixins
from community.bases.api.viewsets import GenericViewSet

# Utils
from community.utils.decorators import swagger_decorator

# Models
from community.apps.boards.models import BoardGroup

# Serializers
from community.apps.boards.api.serializers import BoardGroupListSerializer, BoardGroupWriteListSerializer


# Main Section
class CommunityBoardGroupsViewSet(mixins.ListModelMixin,
                                  GenericViewSet):
    serializers = {
        'default': BoardGroupListSerializer,
    }
    filter_backends = (DjangoFilterBackend,)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return None
        queryset = BoardGroup.available.filter(community=self.kwargs['community_pk'])
        return queryset

    @swagger_auto_schema(**swagger_decorator(tag='01. 커뮤니티',
                                             id='보드 그룹 리스트 조회',
                                             description='## < 보드 그룹 리스트 조회 API 입니다. >',
                                             response={200: BoardGroupListSerializer}))
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)


class CommunityBoardGroupsWriteViewSet(mixins.ListModelMixin,
                                       GenericViewSet):
    serializers = {
        'default': BoardGroupWriteListSerializer,
    }
    filter_backends = (DjangoFilterBackend,)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return None
        queryset = BoardGroup.available.filter(community=self.kwargs['community_pk'])
        return queryset

    @swagger_auto_schema(**swagger_decorator(tag='01. 커뮤니티',
                                             id='보드 그룹 리스트 조회(쓰기 권한)',
                                             description='## < 보드 그룹 리스트 조회(쓰기 권한) API 입니다. >',
                                             response={200: BoardGroupWriteListSerializer}))
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)
