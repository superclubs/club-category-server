# Django
from django.utils.translation import gettext_lazy as _
from django.db.models import F

# Django Rest Framework
from rest_framework import status
from rest_framework.decorators import action

# Third Party
from drf_yasg.utils import swagger_auto_schema

# Utils
from community.utils.api.response import Response
from community.utils.decorators import swagger_decorator
from community.utils.exception_handlers import CustomForbiddenException

# Models
from community.apps.boards.models import BoardGroup

# Serializers
from community.apps.boards.api.serializers import BoardGroupOrderUpdateSerializer, BoardGroupListSerializer


# Main Section
class BoardGroupOrderViewMixin:
    @swagger_auto_schema(**swagger_decorator(tag='02. 보드 그룹 - 어드민',
                                             id='보드 그룹 순서 변경',
                                             description='## < 보드 그룹 순서 변경 API 입니다. >',
                                             request=BoardGroupOrderUpdateSerializer,
                                             response={200: BoardGroupListSerializer}))
    @action(detail=True, methods=['patch'], url_path='order', url_name='board_group_order')
    def board_group_order(self, request, pk=None):
        board_group = self.get_object()
        board_group_order = board_group.order
        request_order = request.data['order']
        if board_group.community.user == request.user:
            board_groups = BoardGroup.available.filter(community=board_group.community.id)
            if board_group_order > request_order:
                board_groups.filter(order__gte=request_order,
                                    order__lte=board_group_order).update(order=F('order') + 1)
            if board_group_order < request_order:
                board_groups.filter(order__gte=board_group_order,
                                    order__lte=request_order).update(order=F('order') - 1)
            board_group.order = request_order
            board_group.save()
            return Response(
                status=status.HTTP_200_OK,
                code=200,
                message=_('ok'),
                data=BoardGroupListSerializer(instance=board_group, context={'request': request}).data
            )
        raise CustomForbiddenException('보드 수정 권한이 없습니다.')
