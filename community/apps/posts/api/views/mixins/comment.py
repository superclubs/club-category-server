# Django
from django.utils.translation import gettext_lazy as _

# Django Rest Framework
from rest_framework import status
from rest_framework.decorators import action

# Third Party
from drf_yasg.utils import swagger_auto_schema

# Serializers
from community.apps.comments.api.serializers import ParentCommentListSerializer, CommentCreateSerializer

# Decorators
from community.utils.decorators import swagger_decorator

# Utils
from community.utils.api.response import Response


# Main Section
class PostCommentViewMixin:

    @swagger_auto_schema(**swagger_decorator(tag='04. 포스트',
                                             id='댓글 생성',
                                             description='## < 댓글 생성 API 입니다. >\n',
                                             request=CommentCreateSerializer,
                                             response={201: ParentCommentListSerializer}
                                             ))
    @action(detail=True, methods=['post'], url_path='comment', url_name='post_comment')
    def post_comment(self, request, pk=None):
        user = request.user
        post = self.get_object()

        profile = post.community.profiles.filter(user=user, is_joined=True, is_active=True, is_deleted=False).first()

        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            instance = serializer.save(community=post.community, user=user, profile=profile, post=post, request=request)

            if instance.image:
                instance.image_url = instance.image.url
                instance.save()

            return Response(
                status=status.HTTP_201_CREATED,
                code=201,
                message=_('ok'),
                data=ParentCommentListSerializer(instance=instance, context={'request': request}).data
            )
