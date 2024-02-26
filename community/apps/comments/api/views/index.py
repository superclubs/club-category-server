# Django
from django.utils.translation import gettext_lazy as _

# Django Rest Framework
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

# Third Party
from drf_yasg.utils import swagger_auto_schema

# Bases
from community.bases.api import mixins
from community.bases.api.viewsets import GenericViewSet

# Mixins
from community.apps.comments.api.views.mixins import CommentLikeViewMixin, CommentReportViewMixin

# Utils
from community.utils.decorators import swagger_decorator
from community.utils.api.response import Response
from community.utils.point import POINT_PER_PARENT_COMMENT

# Models
from community.apps.comments.models import Comment

# Serializers
from community.apps.comments.api.serializers import ChildCommentCreateSerializer, CommentListSerializer, \
    ParentCommentListSerializer, CommentUpdateSerializer


# Main Section
class CommentViewSet(CommentLikeViewMixin,
                     CommentReportViewMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     GenericViewSet):
    serializers = {
        'default': CommentListSerializer,
        'partial_update': CommentUpdateSerializer,
    }
    queryset = Comment.available.all()
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(**swagger_decorator(tag='05. 댓글',
                                             id='댓글 수정',
                                             description='## < 댓글 수정 API 입니다. >',
                                             request=CommentUpdateSerializer,
                                             response={200: ParentCommentListSerializer}
                                             ))
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            instance = serializer.save()

            if instance.parent_comment:
                instance = instance.parent_comment

            return Response(
                status=status.HTTP_200_OK,
                code=200,
                message=_('ok'),
                data=ParentCommentListSerializer(instance=instance, context={'request': request}).data
            )

    @swagger_auto_schema(**swagger_decorator(tag='05. 댓글',
                                             id='댓글 삭제',
                                             description='## < 댓글 삭제 API 입니다. >',
                                             response={204: 'no content'}
                                             ))
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = instance.user
        parent_comment = instance.parent_comment
        post = instance.post

        if instance.comments.filter(is_active=True, is_deleted=False).exists():
            instance.is_deleted = True
            instance.save()

            # Update User Comment Count
            user.decrease_user_comment_count()
            user.save()

            # Update Post Comment Count
            post.decrease_post_comment_count()
            post.save()

            # Update Parent Comment Point
            if parent_comment:
                parent_comment.point = parent_comment.point - POINT_PER_PARENT_COMMENT
                parent_comment.save()

        else:
            self.perform_destroy(instance)

        return Response(
            status=status.HTTP_204_NO_CONTENT,
            code=204,
            message=_('no content'),
        )

    @swagger_auto_schema(**swagger_decorator(tag='05. 댓글',
                                             id='대댓글 생성',
                                             description='## < 대댓글 생성 API 입니다. >\n'
                                                         '### 부모 댓글 `id` 입력',
                                             request=ChildCommentCreateSerializer,
                                             response={201: ParentCommentListSerializer}
                                             ))
    @action(detail=True, methods=['post'], url_path='comment', url_name='comment_comment')
    def comment_comment(self, request, pk=None):
        parent_comment = self.get_object()
        user = request.user

        # 자식 댓글 A에 대댓글 생성 시, A의 부모 댓글로 변경
        if parent_comment.parent_comment:
            parent_comment = parent_comment.parent_comment

        profile = parent_comment.community.profiles.filter(user=user, is_joined=True, is_active=True, is_deleted=False).first()

        serializer = ChildCommentCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            instance = serializer.save(parent_comment=parent_comment, community=parent_comment.community,
                                       user=user, profile=profile, post=parent_comment.post, request=request)

            return Response(
                status=status.HTTP_201_CREATED,
                code=201,
                message=_('ok'),
                data=ParentCommentListSerializer(instance=instance.parent_comment, context={'request': request}).data
            )
