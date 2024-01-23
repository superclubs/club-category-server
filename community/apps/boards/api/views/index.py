# DRF
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

# Third Party
from drf_yasg.utils import swagger_auto_schema

# Bases
from community.bases.api import mixins
from community.bases.api.viewsets import GenericViewSet

# Mixins
from community.apps.boards.api.views.mixins_board_group import BoardGroupBoardViewMixin, BoardGroupOrderViewMixin, \
    BoardGroupMergeViewMixin
from community.apps.boards.api.views.mixins_board import BoardMergeViewMixin, BoardOrderViewMixin

# Filters
from community.apps.boards.api.views.filters.index import BoardFilter

# Utils
from community.utils.api.response import Response
from community.utils.decorators import swagger_decorator
from community.utils.searches import AdvancedSearchFilter

# Models
from community.apps.boards.models import Board, BoardGroup

# Serializers
from community.apps.boards.api.serializers import BoardGroupCreateSerializer, BoardCreateAdminSerializer, \
    BoardRetrieveSerializer, BoardGroupRetrieveSerializer, BoardListSerializer, BoardUpdateAdminSerializer


# Main Section
class BoardGroupViewSet(mixins.RetrieveModelMixin,
                        GenericViewSet):
    serializers = {
        'default': BoardGroupRetrieveSerializer,
    }
    queryset = BoardGroup.available.all()
    filter_backends = (DjangoFilterBackend,)

    @swagger_auto_schema(**swagger_decorator(tag='03. 보드 그룹',
                                             id='보드 그룹 객체 조회',
                                             description='',
                                             response={200: BoardGroupRetrieveSerializer}))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(self, request, *args, **kwargs)


class BoardGroupAdminViewSet(mixins.UpdateModelMixin,
                             mixins.DestroyModelMixin,
                             BoardGroupOrderViewMixin,
                             BoardGroupMergeViewMixin,
                             BoardGroupBoardViewMixin,
                             GenericViewSet):
    serializers = {
        'default': BoardGroupCreateSerializer,
    }
    queryset = BoardGroup.available.all()
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (IsAuthenticated, )

    @swagger_auto_schema(**swagger_decorator(tag='03. 보드 그룹 - 어드민',
                                             id='보드 그룹 수정',
                                             description='',
                                             request=BoardGroupCreateSerializer,
                                             response={200: BoardGroupRetrieveSerializer}))
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(**swagger_decorator(tag='03. 보드 그룹 - 어드민',
                                             id='보드 그룹 객체 삭제',
                                             description='',
                                             response={200: BoardGroupRetrieveSerializer}))
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.posts.exists():
            raise ParseError('Posts must be blank to delete.')
        self.perform_destroy(instance)
        return Response(
            status=status.HTTP_204_NO_CONTENT,
            code=204,
            message='no content',
        )


class BoardsViewSet(mixins.ListModelMixin,
                    GenericViewSet):
    serializers = {
        'default': BoardListSerializer,
    }
    queryset = Board.available.all()
    filter_backends = (DjangoFilterBackend, AdvancedSearchFilter)
    filterset_class = BoardFilter
    search_fields = ('title',)

    @swagger_auto_schema(**swagger_decorator(tag='03. 보드',
                                             id='보드 리스트 조회',
                                             description='## < 보드 리스트 조회 API 입니다. > \n'
                                                         '### `community` : 커뮤니티 id 입력 시, 해당 보드 필터링 \n'
                                                         '### `title` : 보드 타이틀 입력 시, 해당 보드 필터링 \n'
                                                         '### `search`: title 검색 \n'
                                                         '### `or`: 추가 검색어 \n'
                                                         '### `and`: 필수 검색어 \n'
                                                         '### `exclude`: 제외 검색어 \n',
                                             response={200: BoardListSerializer}))
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)


class BoardViewSet(mixins.RetrieveModelMixin,
                   GenericViewSet):
    serializers = {
        'default': BoardRetrieveSerializer,
    }
    queryset = Board.available.all()
    filter_backends = (DjangoFilterBackend,)

    @swagger_auto_schema(**swagger_decorator(tag='03. 보드',
                                             id='보드 객체 조회',
                                             description='',
                                             response={200: BoardRetrieveSerializer}))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(self, request, *args, **kwargs)


class BoardAdminViewSet(mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        BoardMergeViewMixin,
                        BoardOrderViewMixin,
                        GenericViewSet):
    serializers = {
        'default': BoardCreateAdminSerializer,
    }
    queryset = Board.available.all()
    filter_backends = (DjangoFilterBackend,)

    @swagger_auto_schema(**swagger_decorator(tag='03. 보드 - 어드민',
                                             id='보드 수정',
                                             description='',
                                             request=BoardUpdateAdminSerializer,
                                             response={200: BoardRetrieveSerializer}))
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(**swagger_decorator(tag='03. 보드 - 어드민',
                                             id='보드 삭제',
                                             description='',
                                             response={200: BoardRetrieveSerializer}))
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.posts.exists():
            raise ParseError('Posts must be blank to delete.')
        self.perform_destroy(instance)
        return Response(
            status=status.HTTP_204_NO_CONTENT,
            code=204,
            message='no content',
        )
