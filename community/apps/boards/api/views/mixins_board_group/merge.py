# Django
from django.db.models import F
from django.db.models.aggregates import Max

# DRF
from rest_framework.decorators import action
from rest_framework import status

# Third Party
from drf_yasg.utils import swagger_auto_schema

# Utils
from community.utils.api.response import Response
from community.utils.decorators import swagger_decorator

# Models
from community.apps.boards.models import BoardGroup

# Serializers
from community.apps.boards.api.serializers import BoardGroupListSerializer, BoardGroupMergeUpdateSerializer


# TODO Protect 이슈 해결하기
# Main Section
class BoardGroupMergeViewMixin:
    @swagger_auto_schema(**swagger_decorator(tag='03. 보드 그룹 - 어드민',
                                             id='보드 그룹 병합',
                                             description='',
                                             request=BoardGroupMergeUpdateSerializer,
                                             response={200: BoardGroupListSerializer}))
    @action(detail=True, methods=['patch'], url_path='merge', url_name='board_group_merge')
    def board_group_merge(self, request, pk=None):
        board_group = self.get_object()

        request_board_group = BoardGroup.available.get(id=request.data['id'])
        max_board = request_board_group.boards.aggregate(order=Max('order'))
        max_board_order = max_board['order']

        if not max_board_order:
            max_board_order = 0
        board_group.boards.update(board_group=request_board_group, order=F('order') + max_board_order)
        board_group.soft_delete()

        return Response(
            status=status.HTTP_200_OK,
            code=200,
            message='ok',
            data=BoardGroupListSerializer(instance=request_board_group, context={'request': request}).data
        )
