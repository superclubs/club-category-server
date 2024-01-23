# Django
from django.db.models import F

# DRF
from rest_framework.decorators import action
from rest_framework import status

# Third Party
from drf_yasg.utils import swagger_auto_schema

# Utils
from community.utils.api.response import Response
from community.utils.decorators import swagger_decorator
from community.utils.exception_handlers import CustomForbiddenException

# Models
from community.apps.boards.models import Board, BoardGroup

# Serializers
from community.apps.boards.api.serializers import BoardGroupListSerializer, BoardOrderUpdateSerializer


# Main Section
class BoardOrderViewMixin:
    @swagger_auto_schema(**swagger_decorator(tag='03. 보드 - 어드민',
                                             id='보드 순서 변경',
                                             description='',
                                             request=BoardOrderUpdateSerializer,
                                             response={200: BoardGroupListSerializer}))
    @action(detail=True, methods=['patch'], url_path='order', url_name='board_order')
    def board_order(self, request, pk=None):
        board = self.get_object()
        board_order = board.order
        request_order = request.data['order']
        request_board_group = BoardGroup.available.get(id=request.data['board_group'])

        if board.board_group.community.user == request.user:

            board_groups = Board.available.filter(board_group__community__id=board.board_group.community.id,
                                                board_group=board.board_group)
            request_board_groups = Board.available.filter(board_group__community__id=board.board_group.community.id,
                                                        board_group=request_board_group)

            # 보드 그룹이 같을 때
            if board.board_group == request_board_group:
                if board_order > request_order:
                    board_groups.filter(order__gte=request_order,
                                        order__lte=board_order).update(order=F('order') + 1)
                if board_order < request_order:
                    board_groups.filter(order__gte=board_order,
                                        order__lte=request_order).update(order=F('order') - 1)
            # 보드 그룹이 다를 때
            else:
                board_groups.filter(order__gt=board_order).update(order=F('order') - 1)
                request_board_groups.filter(order__gte=request_order).update(order=F('order') + 1)

            board.order = request_order
            board.board_group = request_board_group
            board.save()

            return Response(
                status=status.HTTP_200_OK,
                code=200,
                message='ok',
                data=BoardGroupListSerializer(instance=board.board_group, context={'request': request}).data
            )
        raise CustomForbiddenException('보드 수정 권한이 없습니다.')
