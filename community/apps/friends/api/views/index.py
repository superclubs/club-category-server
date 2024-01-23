# DRF
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError

# Third Party
from drf_yasg.utils import swagger_auto_schema

# Bases
from community.bases.api.viewsets import GenericViewSet
from community.bases.api import mixins

# Utils
from community.utils.decorators import swagger_decorator
from community.utils.api.response import Response

# Models
from community.apps.friends.models import FriendRequest, Friend

# Serializers
from community.apps.friends.api.serializers import FriendRequestCreateSerializer, FriendCreateSerializer, \
    FriendRequestSyncSerializer, FriendSyncSerializer


# Main Section
class FriendRequestViewSet(mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           GenericViewSet):
    serializers = {
        'default': FriendRequestCreateSerializer,
    }
    queryset = FriendRequest.available.all()
    filter_backends = (DjangoFilterBackend,)

    @swagger_auto_schema(**swagger_decorator(tag='05. 친구 요청',
                                             id='친구 요청 생성',
                                             description='',
                                             request=FriendRequestCreateSerializer,
                                             response={201: FriendRequestCreateSerializer}))
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(**swagger_decorator(tag='05. 친구 요청',
                                             id='친구 요청 삭제',
                                             description='',
                                             response={204: 'no content'}))
    def destroy(self, request, *args, **kwargs):
        return super().destroy(self, request, *args, **kwargs)

    @swagger_auto_schema(**swagger_decorator(tag='05. 친구 요청',
                                             id='친구 요청 싱크',
                                             description='',
                                             request=FriendRequestSyncSerializer,
                                             response={200: FriendRequestSyncSerializer}))
    @action(detail=False, methods=['post'])
    def sync(self, request):
        friend_request_id = request.data.pop('id', None)
        friend_request = FriendRequest.available.filter(id=friend_request_id).first()

        if not friend_request:
            raise ParseError('존재하지 않는 친구 요청 데이터')

        serializer = FriendRequestSyncSerializer(instance=friend_request, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                status=status.HTTP_200_OK,
                code=200,
                message='ok',
                data=FriendRequestSyncSerializer(instance=friend_request, context={'request': request}).data
            )


class FriendViewSet(mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    GenericViewSet):
    serializers = {
        'default': FriendCreateSerializer,
    }
    queryset = Friend.available.all()
    filter_backends = (DjangoFilterBackend,)

    @swagger_auto_schema(**swagger_decorator(tag='05. 친구',
                                             id='친구 생성',
                                             description='',
                                             request=FriendCreateSerializer,
                                             response={201: FriendCreateSerializer}))
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(**swagger_decorator(tag='05. 친구',
                                             id='친구 삭제',
                                             description='',
                                             response={204: 'no content'}))
    def destroy(self, request, *args, **kwargs):
        return super().destroy(self, request, *args, **kwargs)

    @swagger_auto_schema(**swagger_decorator(tag='05. 친구',
                                             id='친구 생성',
                                             description='',
                                             request=FriendSyncSerializer,
                                             response={200: FriendSyncSerializer}))
    @action(detail=False, methods=['post'])
    def sync(self, request):
        friend_id = request.data.pop('id', None)
        friend = Friend.available.filter(id=friend_id).first()

        if not friend:
            raise ParseError('존재하지 않는 친구 데이터')

        serializer = FriendSyncSerializer(instance=friend, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                status=status.HTTP_200_OK,
                code=200,
                message='ok',
                data=FriendSyncSerializer(instance=friend, context={'request': request}).data
            )
