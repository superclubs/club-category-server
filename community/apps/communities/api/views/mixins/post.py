# Python
from datetime import timedelta, datetime

# Django
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now

# Django Rest Framework
from rest_framework.exceptions import ParseError
from rest_framework import status
from rest_framework.decorators import action

# Third Party
from drf_yasg.utils import swagger_auto_schema

# Utils
from community.utils.api.response import Response
from community.utils.decorators import swagger_decorator

# Models
from community.apps.communities.models import Community
from community.apps.posts.models import Post

# Serializers
from community.apps.posts.api.serializers import PostCreateSerializer, PostRetrieveSerializer


# Main Section
class CommunityPostViewMixin:
    @swagger_auto_schema(**swagger_decorator(tag='01. 커뮤니티',
                                             id='포스트 생성',
                                             description='',
                                             request=PostCreateSerializer,
                                             response={201: PostRetrieveSerializer}
                                             ))
    @action(detail=True, methods=['post'], url_path='post', url_name='community_post')
    def community_post(self, request, pk=None):
        user = request.user
        community = self.get_object()
        tags = request.data.pop('tags', None)
        board_id = request.data.pop('board', None)
        board = community.boards.filter(id=board_id, is_active=True, is_deleted=False).first()
        profile = user.profiles.filter(community=community, is_joined=True, is_active=True, is_deleted=False).first()
        reserved_at = request.data.pop('reserved_at', None)
        boomed_period = request.data.pop('boomed_period', None)
        is_reserved = Post._meta.get_field('is_reserved').get_default()
        is_boomed = Post._meta.get_field('is_boomed').get_default()
        boomed_at = Post._meta.get_field('boomed_at').get_default()

        if reserved_at:
            if str(now()) > reserved_at:
                raise ParseError('과거로 예약할 수 없습니다.')
            is_reserved = True

        if boomed_period:
            if reserved_at:
                boomed_at = datetime.fromisoformat(reserved_at) + timedelta(minutes=int(boomed_period))
            else:
                boomed_at = now() + timedelta(minutes=int(boomed_period))

            is_boomed = True

        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            instance = serializer.save(community=community, user=user, profile=profile, board=board,
                                       reserved_at=reserved_at, is_reserved=is_reserved,
                                       is_boomed=is_boomed, boomed_at=boomed_at, boomed_period=boomed_period)

            if tags:
                for index, tag in enumerate(tags):
                    if tag == '':
                        pass
                    else:
                        instance.create_post_tag(index=index, tag=tag)

            return Response(
                status=status.HTTP_201_CREATED,
                code=201,
                message=_('ok'),
                data=PostRetrieveSerializer(instance=instance).data
            )

    @swagger_auto_schema(**swagger_decorator(tag='01. 커뮤니티',
                                             id='임시글 일괄 삭제',
                                             description='',
                                             response={204: 'no content'}
                                             ))
    @action(methods=['delete'], detail=True, url_path='posts/temporary', url_name='community_post_temporary')
    def community_post_temporary(self, request, pk):
        community = Community.available.filter(id=pk).first()
        posts = community.posts.filter(is_temporary=True, user=request.user, is_active=True, is_deleted=False)
        for post in posts:
            post.soft_delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT,
            code=204,
            message=_('no content'),
        )
