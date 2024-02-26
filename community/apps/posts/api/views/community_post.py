# Django
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

# Django Rest Framework
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend

# Third Party
from drf_yasg.utils import swagger_auto_schema

# Utils
from community.utils.orderings import NullsLastOrderingFilter
from community.utils.api.response import Response

# Filters
from community.apps.posts.api.views.filters.index import PostsAdminFilter, ClubPostFilter

# Bases
from community.bases.api import mixins
from community.bases.api.viewsets import GenericViewSet

# Decorators
from community.utils.decorators import swagger_decorator

# Serializers
from community.apps.posts.api.serializers import PostListSerializer

# Models
from community.apps.posts.models import Post


# Main Section
class CommunityPostsViewSet(mixins.ListModelMixin,
                            GenericViewSet):
    serializers = {
        'default': PostListSerializer,
    }
    filter_backends = (DjangoFilterBackend, NullsLastOrderingFilter,)
    filterset_class = ClubPostFilter
    ordering_fields = ('created', 'live_rank', 'weekly_rank', 'monthly_rank', 'rising_rank')

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return None
        queryset = Post.active.filter_readonly(user=self.request.user)
        queryset = queryset.filter(community=self.kwargs['community_pk'])

        ordering = self.request.GET.get('ordering', None)
        if ordering and ordering == 'rising_rank':
            q1 = Q(public_type='PUBLIC')
            q2 = Q(is_secret=True)
            queryset = queryset.exclude(~q1 | q2)

        queryset = PostListSerializer().prefetch_related(queryset, user=self.request.user)
        return queryset

    @swagger_auto_schema(**swagger_decorator(tag='01. 커뮤니티',
                                             id='포스트 리스트 조회',
                                             description='## < 포스트 리스트 조회 API 입니다. >\n'
                                                         '### `profile` : 프로필 id 입력 시, 해당 프로필이 업로드한 포스트 필터링 \n'
                                                         '### `tag_title` : tag title 필터링 \n'
                                                         '### `public_type` : PUBLIC, FRIEND, ONLY_ME 필터링 \n'
                                                         '### `public_type__not` : PUBLIC, FRIEND, ONLY_ME 제외 필터링 \n'
                                                         '### `is_temporary` : true 입력 시, 임시글 필터링 \n'
                                                         '### `is_notice` : true 입력 시, 공지글 필터링 \n'
                                                         '### `is_event` : true 입력 시, 이벤트글 필터링 \n'
                                                         '### `is_bookmarked` : true 입력 시, 북마크 포스트 필터링 \n'
                                                         '### `ordering` : created, live_rank, week_rank, month_rank, rising_rank',
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


class CommunityPostsAdminViewSet(mixins.ListModelMixin,
                                 GenericViewSet):
    serializers = {
        'default': PostListSerializer,
    }
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PostsAdminFilter
    ordering_fields = ['reported_count']

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return None
        queryset = Post.available.all()
        queryset = queryset.filter(community=self.kwargs['community_pk'])
        queryset = PostListSerializer.prefetch_related(queryset)
        return queryset

    @swagger_auto_schema(**swagger_decorator(tag='01. 커뮤니티 - 어드민',
                                             id='포스트 리스트 조회',
                                             description='## < 포스트 리스트 조회 API 입니다. >\n'
                                                         '### `profile` : 프로필 id 입력 시, 해당 프로필이 업로드한 포스트 필터링 \n'
                                                         '### `tag_title` : tag title 필터링 \n'
                                                         '### `public_type` : PUBLIC, FRIEND, ONLY_ME 필터링 \n'
                                                         '### `public_type__not` : PUBLIC, FRIEND, ONLY_ME 제외 필터링 \n'
                                                         '### `is_temporary` : true 입력 시, 임시글 필터링 \n'
                                                         '### `is_notice` : true 입력 시, 공지글 필터링 \n'
                                                         '### `is_event` : true 입력 시, 이벤트글 필터링 \n'
                                                         '### `ordering` : created, live_rank, week_rank, month_rank, rising_rank',
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
