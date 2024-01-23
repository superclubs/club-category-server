# DRF
from rest_framework.exceptions import ParseError
from rest_framework.decorators import action
from rest_framework import status

# Third Party
from drf_yasg.utils import swagger_auto_schema

# Utils
from community.utils.api.response import Response
from community.utils.decorators import swagger_decorator

# Models
from community.apps.boards.models import Board

# Serializers
from community.apps.boards.api.serializers import BoardGroupListSerializer, BoardMergeUpdateSerializer


# Main Section
class BoardMergeViewMixin:
    @swagger_auto_schema(**swagger_decorator(tag='03. 보드 - 어드민',
                                             id='보드 병합',
                                             description='',
                                             request=BoardMergeUpdateSerializer,
                                             response={200: BoardGroupListSerializer}))
    @action(detail=True, methods=['patch'], url_path='merge', url_name='board_merge')
    def board_merge(self, request, pk=None):
        board = self.get_object()

        request_board = Board.available.get(id=request.data['id'])

        if board.posts.count() + request_board.posts.count() > 10:
            raise ParseError('There are more than 10 posts on both boards.')

        request_board.write_permission = min(request_board.write_permission, board.write_permission)
        request_board.read_permission = min(request_board.read_permission, board.read_permission)
        request_board.save()

        board.posts.update(board=request_board)
        board.soft_delete()

        return Response(
            status=status.HTTP_200_OK,
            code=200,
            message='ok',
            data=BoardGroupListSerializer(instance=request_board.board_group, context={'request': request}).data
        )
