# DRF
from rest_framework import status
from rest_framework.decorators import action

# Third Party
from drf_yasg.utils import swagger_auto_schema

# Utils
from community.utils.api.response import Response
from community.utils.decorators import swagger_decorator

# Models
from community.apps.communities.models import Community


# Not use
# Main Section
class CommunityPostViewMixin:
    @swagger_auto_schema(**swagger_decorator(tag='02. 커뮤니티',
                                             id='임시글 일괄 삭제',
                                             description='',
                                             response={204: 'no content'}
                                             ))
    @action(methods=['delete'], detail=True, url_path='posts/temporary', url_name='community_post_temporary')
    def community_post_temporary(self, request, pk):
        community = Community.available.filter(id=pk).first()
        posts = community.posts.filter(is_temporary=True, user=request.user, is_active=True, is_deleted=False).all()

        if posts:
            for post in posts:
                post.soft_delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT,
            code=204,
            message='no content',
        )
