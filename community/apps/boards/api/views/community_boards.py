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
from community.apps.boards.models import Board

# Serializers
from community.apps.boards.api.serializers import BoardListSerializer


# Main Section
class CommunityBoardsViewSet(mixins.ListModelMixin,
                             GenericViewSet):
    serializers = {
        'default': BoardListSerializer,
    }
    filter_backends = (DjangoFilterBackend,)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return None
        queryset = Board.available.filter(community=self.kwargs["community_pk"])
        return queryset

    @swagger_auto_schema(**swagger_decorator(tag='02. 커뮤니티',
                                             id='보드 리스트 조회',
                                             description='',
                                             response={200: BoardListSerializer}))
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)


class CommunityBoardsAdminViewSet(mixins.ListModelMixin,
                                  GenericViewSet):
    serializers = {
        'default': BoardListSerializer,
    }
    filter_backends = (DjangoFilterBackend,)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return None
        # 비활성화된 객체는 보여야하기 때문에 objects
        queryset = Board.available.filter(community=self.kwargs["community_pk"], is_deleted=False)
        return queryset

    @swagger_auto_schema(**swagger_decorator(tag='02. 커뮤니티 - 어드민',
                                             id='보드 리스트 조회',
                                             description='',
                                             response={200: BoardListSerializer}))
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)
