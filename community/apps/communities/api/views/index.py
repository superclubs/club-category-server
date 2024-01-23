# DRF
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
    CommunityDashboardViewMixin, CommunityBoardViewMixin

# Filters
from community.apps.communities.api.views.filters import CommunitiesFilter, CommunityFilter

# Utils
from community.utils.decorators import swagger_decorator
from community.utils.api.response import Response
from community.utils.searches import AdvancedSearchFilter

# Serializers
from community.apps.communities.api.serializers import CommunityListSerializer, CommunityRetrieveSerializer, \
    CommunityUpdateAdminSerializer

# Models
from community.apps.communities.models import Community
from community.apps.profiles.models import Profile


# Main Section
class CommunityViewSet(mixins.RetrieveModelMixin,
                       CommunityDashboardViewMixin,
                       GenericViewSet):
    serializers = {
        'default': CommunityRetrieveSerializer,
    }
    queryset = Community.available.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CommunityFilter
    pagination_class = None

    @swagger_auto_schema(**swagger_decorator(tag='02. 커뮤니티',
                                             id='커뮤니티 객체 조회',
                                             description='',
                                             response={200: CommunityRetrieveSerializer}
                                             ))
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        user = request.user

        if user.id:
            profile = instance.profiles.filter(user=user, is_active=True, is_deleted=False).first()
            if not profile:
                profile = Profile.objects.create(community=instance, user=user)

            instance.create_community_visit(profile)

        return Response(
            status=status.HTTP_200_OK,
            code=200,
            message='ok',
            data=serializer.data
        )


class CommunitiesViewSet(mixins.ListModelMixin,
                         GenericViewSet):
    serializers = {
        'default': CommunityListSerializer,
    }
    queryset = Community.available.all()
    filter_backends = (AdvancedSearchFilter, DjangoFilterBackend)
    ordering_fields = ('created', 'order')
    filterset_class = CommunitiesFilter
    pagination_class = None

    @swagger_auto_schema(**swagger_decorator(tag='02. 커뮤니티',
                                             id='커뮤니티 리스트 조회',
                                             description='## < 커뮤니티 리스트 조회 API 입니다. > \n'
                                                         '### ordering : `created (생성순)` \n'
                                                         '### `depth` : depth 로 필터링 가능합니다.\n'
                                                         '### `community_id` : community_id 로 필터링 가능합니다.\n',
                                             response={200: CommunityListSerializer}
                                             ))
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)


class CommunityAdminViewSet(mixins.UpdateModelMixin,
                            CommunityImageViewMixin,
                            CommunityBoardGroupViewMixin,
                            CommunityBoardViewMixin,
                            GenericViewSet):
    serializers = {
        'default': CommunityUpdateAdminSerializer,
    }
    queryset = Community.available.all()
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(**swagger_decorator(tag='02. 커뮤니티 - 어드민',
                                             id='커뮤니티 수정',
                                             description='',
                                             request=CommunityUpdateAdminSerializer,
                                             response={200: 'ok'}
                                             ))
    def partial_update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(
            status=status.HTTP_200_OK,
            code=200,
            message='ok',
            data=CommunityRetrieveSerializer(instance=instance, context={'request': request}).data
        )
