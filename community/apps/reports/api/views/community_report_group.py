# DRF
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

# Third Party
from drf_yasg.utils import swagger_auto_schema

# Bases
from community.bases.api import mixins
from community.bases.api.viewsets import GenericViewSet

# Filters
from community.apps.reports.api.views.filters import ReportGroupFilter

# Utils
from community.utils.decorators import swagger_decorator

# Models
from community.apps.reports.models import ReportGroup

# Serializers
from community.apps.reports.api.serializers import ReportGroupListSerializer


# Main Section
class CommunityReportGroupsAdminViewSet(mixins.ListModelMixin,
                                        GenericViewSet):
    serializers = {
        'default': ReportGroupListSerializer,
    }
    filter_backends = (SearchFilter, DjangoFilterBackend, OrderingFilter)
    search_fields = ('username', 'contents', 'post__content')
    filterset_class = ReportGroupFilter
    ordering_fields = ('id', 'username', 'contents', 'is_deactivated', 'reported_count', 'deactivated_at')

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return None
        queryset = ReportGroup.available.filter(community=self.kwargs["community_pk"])
        return queryset

    @swagger_auto_schema(**swagger_decorator(tag='02. 커뮤니티 - 어드민',
                                             id='신고 리스트 조회',
                                             description='## < 신고 리스트 조회 API 입니다. > \n'
                                                         '### `search`: username, contents, post_content 검색 \n'
                                                         '### `profile`: 프로필 id 필터링 \n'
                                                         '### `is_post`: true 입력 시, 포스트 필터링 \n'
                                                         '### `is_comment`: true 입력 시, 댓글 필터링 \n'
                                                         '### `is_deactivated`: true 입력 시, 비활성화 컨텐츠 필터링 \n'
                                                         '### `ordering`: id, username, contents, is_deactivated, reported_count, deactivated_at \n',
                                             response={200: ReportGroupListSerializer}
                                             ))
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)
