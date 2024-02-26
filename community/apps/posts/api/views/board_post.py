# Django
from django.utils.translation import gettext_lazy as _

# Django Rest Framework
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend

# Third Party
from drf_yasg.utils import swagger_auto_schema

# Filters
from community.apps.posts.api.views.filters import BoardPostFilter

# Bases
from community.bases.api import mixins
from community.bases.api.viewsets import GenericViewSet

# Decorators
from community.utils.decorators import swagger_decorator

# Serializers
from community.apps.posts.api.serializers import PostListSerializer

# Models
from community.apps.posts.models import Post
from community.apps.boards.models import Board

# Utils
from community.utils.searches import AdvancedSearchFilter
from community.utils.orderings import NullsLastOrderingFilter
from community.utils.api.response import Response


# Main Section
class BoardPostsViewSet(mixins.ListModelMixin,
                        GenericViewSet):
    serializers = {
        'default': PostListSerializer,
    }
    filter_backends = (DjangoFilterBackend, AdvancedSearchFilter, NullsLastOrderingFilter)
    filterset_class = BoardPostFilter
    search_fields = ('title', 'content', 'post_tags__title')
    ordering_fields = ('created', 'live_rank', 'weekly_rank', 'monthly_rank')

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return None
        board_id = self.kwargs['board_pk']
        board = Board.available.get(id=board_id)
        if board.title == 'All':
            queryset = Post.active.filter_readonly(user=self.request.user)
            queryset = queryset.filter(community=board.community)
        else:
            queryset = Post.active.filter_readonly(user=self.request.user)
            queryset = queryset.filter(board=board_id)

        queryset = PostListSerializer().prefetch_related(queryset, user=self.request.user)
        return queryset

    @swagger_auto_schema(**swagger_decorator(tag='03. 보드',
                                             id='포스트 리스트 조회',
                                             description='## < 포스트 리스트 조회 API 입니다. >\n'
                                                         '### `date`: week, month, year 기간 내 생성된 커뮤니티 필터링 \n'
                                                         '### `public_type__not` : PUBLIC, FRIEND, ONLY_ME 제외 필터링 \n'
                                                         '### `is_temporary` : true 입력 시, 임시글 필터링 \n'
                                                         '### `is_notice` : true 입력 시, 공지글 필터링 \n'
                                                         '### `is_event` : true 입력 시, 이벤트글 필터링 \n'
                                                         '### `ordering` : created, live_rank, weekly_rank, monthly_rank, rising_rank \n'
                                                         '### `search` : title, content, tag_title 검색 \n'
                                                         '### `or`: 추가 검색어 \n'
                                                         '### `and`: 필수 검색어 \n'
                                                         '### `exclude`: 제외 검색어 \n',
                                             response={200: PostListSerializer}
                                             ))
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)

        return Response(
            status=status.HTTP_200_OK,
            code=200,
            message=_('ok'),
            data=serializer.data
        )
