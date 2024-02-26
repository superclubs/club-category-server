# Django
from django.utils.translation import gettext_lazy as _

# Django Rest Framework
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

# Third Party
from drf_yasg.utils import swagger_auto_schema, no_body

# Bases
from community.bases.api import mixins
from community.bases.api.viewsets import GenericViewSet

# Mixins
from community.apps.posts.api.views.mixins import PostBookmarkViewMixin, PostCommentViewMixin, \
    PostLikeViewMixin, PostReportViewMixin, PostShareViewMixin, PostTagViewMixin

# Filters
from community.apps.posts.api.views.filters import PostFilter

# Utils
from community.utils.api.response import Response
from community.utils.decorators import swagger_decorator
from community.utils.orderings import NullsLastOrderingFilter
from community.utils.searches import AdvancedSearchFilter

# Models
from community.apps.posts.models import Post

# Serializers
from community.apps.posts.api.serializers import PostRetrieveSerializer, PostUpdateSerializer, PostListSerializer


# Main Section
class PostsViewSet(mixins.ListModelMixin,
                   GenericViewSet):
    serializers = {
        'default': PostListSerializer,
    }
    filter_backends = (DjangoFilterBackend, AdvancedSearchFilter, NullsLastOrderingFilter)
    filterset_class = PostFilter
    search_fields = ('title', 'content', 'post_tags__title')
    ordering_fields = ('created', 'live_rank', 'weekly_rank', 'monthly_rank', 'rising_rank')

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return None

        user = self.request.user
        queryset = Post.active.filter_readonly(user=user).filter(is_default=False)
        queryset = PostListSerializer().prefetch_related(queryset, user=self.request.user)
        return queryset

    @swagger_auto_schema(**swagger_decorator(tag='04. 포스트',
                                             id='포스트 리스트 조회',
                                             description='## < 포스트 리스트 조회 API 입니다. >\n'
                                                         '### `date`: week, month, year 기간 내 생성된 커뮤니티 필터링 \n'
                                                         '### `profile` : 프로필 id 입력 시, 해당 프로필이 업로드한 포스트 필터링 \n'
                                                         '### `profile_liked` : 프로필 id 입력 시, 좋아요 누른 포스트 필터링 \n'
                                                         '### `profile_commented` : 프로필 id 입력 시, 댓글 단 포스트 필터링 \n'
                                                         '### `tag_title` : tag title 필터링 \n'
                                                         '### `public_type` : PUBLIC, FRIEND, ONLY_ME 필터링 \n'
                                                         '### `public_type__not` : PUBLIC, FRIEND, ONLY_ME 제외 필터링 \n'
                                                         '### `is_temporary` : true 입력 시, 임시글 필터링 \n'
                                                         '### `is_notice` : true 입력 시, 공지글 필터링 \n'
                                                         '### `is_joined` : true 입력 시, 가입한 커뮤니티의 포스트 필터링 \n'
                                                         '### `is_subscribed` : true 입력 시, 구독 포스트 필터링 \n'
                                                         '### `ordering` : created, live_rank, weekly_rank, monthly_rank, rising_rank \n'
                                                         '### `search` : title, content, tag_title 검색 \n'
                                                         '### `or`: 추가 검색어 \n'
                                                         '### `and`: 필수 검색어 \n'
                                                         '### `exclude`: 제외 검색어',
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


class PostViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  PostCommentViewMixin,
                  PostTagViewMixin,
                  PostShareViewMixin,
                  PostBookmarkViewMixin,
                  PostLikeViewMixin,
                  PostReportViewMixin,
                  GenericViewSet):
    serializers = {
        'default': PostRetrieveSerializer,
        'partial_update': PostUpdateSerializer,
    }
    filter_backends = (DjangoFilterBackend,)

    queryset = Post.available.all()

    @swagger_auto_schema(**swagger_decorator(tag='04. 포스트',
                                             id='포스트 조회',
                                             description='## < 포스트 조회 API 입니다. >',
                                             response={200: PostRetrieveSerializer}
                                             ))
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        user = request.user
        if user.id:
            instance.create_post_visit(user)
        return Response(
            status=status.HTTP_200_OK,
            code=200,
            message=_('ok'),
            data=serializer.data
        )

    @swagger_auto_schema(**swagger_decorator(tag='04. 포스트',
                                             id='포스트 수정',
                                             description='## < 포스트 수정 API 입니다. >',
                                             request=PostUpdateSerializer,
                                             response={200: PostUpdateSerializer}
                                             ))
    def partial_update(self, request, *args, **kwargs):
        post = self.get_object()
        user = request.user
        serializer = self.get_serializer(instance=post, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            post = serializer.save()
            community = post.community

            return Response(
                status=status.HTTP_200_OK,
                code=200,
                message=_('ok'),
                data=PostUpdateSerializer(instance=post, context={'request': request}).data
            )

    @swagger_auto_schema(**swagger_decorator(tag='04. 포스트',
                                             id='포스트 삭제',
                                             description='## < 포스트 삭제 API 입니다. >',
                                             response={204: 'no content'}
                                             ))
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.soft_delete(request=self.request)
        return Response(
            status=status.HTTP_204_NO_CONTENT,
            code=204,
            message=_('no content'),
        )

    @swagger_auto_schema(**swagger_decorator(tag='04. 포스트',
                                             id='임시글 객체 삭제',
                                             description='## < 임시글 객체 삭제 API 입니다. >',
                                             response={204: 'no content'}
                                             ))
    @action(methods=['delete'], detail=True, url_path='temporary', url_name='post_temporary')
    def post_temporary(self, request, pk):
        post = self.get_object()
        if not post.is_temporary:
            raise ParseError('임시글이 아닙니다.')
        post.soft_delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT,
            code=204,
            message=_('no content'),
        )

    @swagger_auto_schema(**swagger_decorator(tag='04. 포스트',
                                             id='포스트 킵',
                                             description='## < 포스트 킵 API 입니다. >',
                                             request=no_body,
                                             response={200: 'ok'}
                                             ))
    @action(detail=True, methods=['post'], url_path='keep', url_name='post_keep')
    def post_keep(self, request, pk=None):
        post = self.get_object()

        if post.public_type == 'ONLY_ME':
            raise ParseError('이미 킵한 포스트입니다.')

        post.public_type = 'ONLY_ME'
        post.save()
        return Response(
            status=status.HTTP_200_OK,
            code=200,
            message=_('ok'),
        )

    @swagger_auto_schema(**swagger_decorator(tag='04. 포스트',
                                             id='포스트 언킵',
                                             description='## < 포스트 언킵 API 입니다. >',
                                             request=no_body,
                                             response={200: 'ok'}
                                             ))
    @action(detail=True, methods=['post'], url_path='unkeep', url_name='post_unkeep')
    def post_unkeep(self, request, pk=None):
        post = self.get_object()

        if not post.public_type == 'ONLY_ME':
            raise ParseError('킵한 포스트이 아닙니다.')

        post.public_type = 'PUBLIC'
        post.save()
        return Response(
            status=status.HTTP_200_OK,
            code=200,
            message=_('ok'),
        )
