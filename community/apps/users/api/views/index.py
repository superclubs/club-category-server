# Django
from django.db.models import Q

# DRF
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from rest_framework.filters import SearchFilter

# Third Party
from drf_yasg.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend

# Bases
from community.bases.api.viewsets import GenericViewSet
from community.bases.api import mixins

# Utils
from community.utils.api.response import Response
from community.utils.decorators import swagger_decorator

# Models
from community.apps.users.models import User

# Serializers
from community.apps.users.api.serializers import UserMeSerializer, UserSerializer, UserSyncSerializer, \
    UserPasswordSerializer


# Main Section
class UsersViewSet(mixins.ListModelMixin,
                   GenericViewSet):
    serializers = {
        'default': UserSerializer,
    }
    queryset = User.available.exclude(Q(username=None) | Q(username=''))
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('username',)

    @swagger_auto_schema(**swagger_decorator(tag='01. 유저',
                                             id='유저 리스트 조회',
                                             description='',
                                             response={200: UserSerializer}
                                             ))
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)


class UserViewSet(GenericViewSet):
    serializers = {
        'default': UserSerializer,
    }
    queryset = User.available.all()
    filter_backends = (DjangoFilterBackend,)
    pagination_class = None

    @swagger_auto_schema(**swagger_decorator(tag='01. 유저',
                                             id='내 정보',
                                             description='',
                                             response={200: UserMeSerializer}
                                             ))
    @action(detail=False, methods=['get'])
    def me(self, request):
        return Response(
            status=status.HTTP_200_OK,
            code=200,
            message='ok',
            data=UserMeSerializer(instance=request.user, context={'request': request}).data
        )

    @swagger_auto_schema(**swagger_decorator(tag='01. 유저',
                                             id='유저 싱크',
                                             description='',
                                             request=UserSyncSerializer,
                                             response={200: UserSyncSerializer}
                                             ))
    @action(detail=False, methods=['post'])
    def sync(self, request):
        user_id = request.data.pop('id', None)
        user = User.available.filter(id=user_id).first()

        if not user:
            raise ParseError('존재하지 않는 유저입니다.')

        serializer = UserSyncSerializer(instance=user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                status=status.HTTP_200_OK,
                code=200,
                message='ok',
                data=UserSyncSerializer(instance=request.user, context={'request': request}).data
            )


class UserAdminViewSet(GenericViewSet):
    serializers = {
        'default': UserSerializer,
        'set_admin': UserPasswordSerializer,
        'change_password': UserPasswordSerializer,
    }
    queryset = User.available.all()
    filter_backends = (DjangoFilterBackend,)

    @swagger_auto_schema(**swagger_decorator(tag='01. 유저 - 어드민',
                                             id='어드민 권한 부여',
                                             description='## < 어드민 권한 부여 API 입니다. >\n'
                                                         '### `Common server 어드민 사이트에서 비밀번호 변경 시 호출됩니다.`',
                                             request=UserPasswordSerializer,
                                             response={200: UserSerializer}
                                             ))
    def set_admin(self, request):
        user_id = request.data.get('id', None)
        password = request.data.get('password', None)

        user = User.available.filter(id=user_id).first()
        if not user:
            raise ParseError('존재하지 않는 유저입니다.')

        user.admin_set(password)

        return Response(
            status=status.HTTP_200_OK,
            code=200,
            message='ok',
        )

    @swagger_auto_schema(**swagger_decorator(tag='01. 유저 - 어드민',
                                             id='어드민 비밀번호 변경',
                                             description='',
                                             request=UserPasswordSerializer,
                                             response={200: 'ok'}
                                             ))
    @action(detail=True, methods=['patch'], url_path='password', url_name='password_change')
    def password_change(self, request, pk=None):
        user = self.get_object()
        password = request.data.get('password', None)

        user.change_password(password)

        return Response(
            status=status.HTTP_200_OK,
            code=200,
            message='ok'
        )
