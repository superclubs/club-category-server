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

# Utils
from community.utils.api.response import Response
from community.utils.decorators import swagger_decorator

# Models
from community.apps.reports.models.index import ReportChoice

# Serializers
from community.apps.reports.api.serializers import ReportChoiceListSerializer, ReportChoiceUpdateSerializer


# Main Section
class CommunityReportChoiceAdminViewSet(mixins.UpdateModelMixin,
                                        mixins.DestroyModelMixin,
                                        GenericViewSet):
    serializers = {
        'default': ReportChoiceListSerializer,
        'partial_update': ReportChoiceUpdateSerializer,
    }
    queryset = ReportChoice.available.all()
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(**swagger_decorator(tag='13. 신고 - 어드민',
                                             id='신고 사유 수정',
                                             description='',
                                             request=ReportChoiceUpdateSerializer,
                                             response={200: ReportChoiceListSerializer}
                                             ))
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(**swagger_decorator(tag='13. 신고 - 어드민',
                                             id='신고 사유 삭제',
                                             description='',
                                             response={204: 'no content'}
                                             ))
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_default:
            raise ParseError('기본 신고 사유는 삭제할 수 없습니다.')
        self.perform_destroy(instance)
        return Response(
            status=status.HTTP_204_NO_CONTENT,
            code=204,
            message='no content',
        )


class CommunityReportChoicesViewSet(mixins.ListModelMixin,
                                    GenericViewSet):
    serializers = {
        'default': ReportChoiceListSerializer,
    }
    filter_backends = (DjangoFilterBackend,)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return None
        queryset = ReportChoice.available.filter(community=self.kwargs["community_pk"])
        return queryset

    @swagger_auto_schema(**swagger_decorator(tag='02. 커뮤니티',
                                             id='신고 사유 리스트 조회',
                                             description='',
                                             response={200: ReportChoiceListSerializer}
                                             ))
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)
