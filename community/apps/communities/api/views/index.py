# Django
from django.utils.translation import gettext_lazy as _
from django.db.models import Prefetch

# Django Rest Framework
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

# Third Party
from drf_yasg.utils import swagger_auto_schema

# Bases
from community.bases.api import mixins
from community.bases.api.viewsets import GenericViewSet

# Mixins
from community.apps.communities.api.views.mixins import CommunityImageViewMixin, CommunityBoardGroupViewMixin, \
    CommunityPostViewMixin

# Filters
from community.apps.communities.api.views.filters import CommunitiesFilter, CommunityFilter

# Utils
from community.utils.decorators import swagger_decorator
from community.utils.api.response import Response
from community.utils.searches import AdvancedSearchFilter
from community.utils.orderings import NullsLastOrderingFilter

# Models
from community.apps.communities.models import Community
from community.apps.posts.models import Post
from community.apps.badges.models import Badge

# Serializers
from community.apps.communities.api.serializers import CommunityListSerializer, CommunityRetrieveSerializer, \
    CommunityUpdateAdminSerializer


# Main Section
class CommunityViewSet(mixins.RetrieveModelMixin,
                       CommunityPostViewMixin,
                       GenericViewSet):
    serializers = {
        'default': CommunityRetrieveSerializer,
    }
    queryset = Community.available.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CommunityFilter
    pagination_class = None

    @swagger_auto_schema(**swagger_decorator(tag='01. 커뮤니티',
                                             id='커뮤니티 객체 조회',
                                             description='## < 커뮤니티 객체 조회 API 입니다. >',
                                             response={200: CommunityRetrieveSerializer}
                                             ))
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        user = request.user
        if user.id:
            instance.create_community_visit(user)

        return Response(
            status=status.HTTP_200_OK,
            code=200,
            message=_('ok'),
            data=serializer.data
        )


class CommunitiesViewSet(mixins.ListModelMixin,
                         GenericViewSet):
    serializer_class = CommunityListSerializer
    queryset = Community.available.all()
    filter_backends = (AdvancedSearchFilter, DjangoFilterBackend, NullsLastOrderingFilter,)
    filterset_class = CommunitiesFilter
    search_fields = ('title', 'description', 'address', 'community_tags__title')
    ordering_fields = ('point', 'created', 'live_rank', 'weekly_rank', 'monthly_rank', 'rising_rank')

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return None

        queryset = Community.available.filter(is_active=True, is_deleted=False).select_related('category')
        user = self.request.user

        if user.id:
            badges = Badge.available.order_by('id')
            posts = Post.available.filter(is_temporary=False)

            queryset = queryset.prefetch_related(
                Prefetch('badges', queryset=badges),
                Prefetch('posts', queryset=posts),
            )

        return queryset

    @swagger_auto_schema(**swagger_decorator(tag='01. 커뮤니티',
                                             id='커뮤니티 리스트 조회',
                                             description='## < 커뮤니티 리스트 조회 API 입니다. > \n'
                                                         '### `ordering`: point, created, live_rank, weekly_rank, monthly_rank, rising_rank \n'
                                                         '### `search`: title, description, address, tag_title 검색 \n'
                                                         '### `or`: 추가 검색어 \n'
                                                         '### `and`: 필수 검색어 \n'
                                                         '### `exclude`: 제외 검색어 \n',
                                             response={200: CommunityListSerializer}
                                             ))
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)


class CommunityAdminViewSet(mixins.UpdateModelMixin,
                            CommunityImageViewMixin,
                            CommunityBoardGroupViewMixin,
                            GenericViewSet):
    serializers = {
        'partial_update': CommunityUpdateAdminSerializer,
    }
    queryset = Community.available.all()
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(**swagger_decorator(tag='01. 커뮤니티 - 어드민',
                                             id='커뮤니티 수정',
                                             description='## < 커뮤니티 수정 API 입니다. >',
                                             request=CommunityUpdateAdminSerializer,
                                             response={200: CommunityUpdateAdminSerializer}
                                             ))
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
