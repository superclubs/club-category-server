# Django
from django.db.models import (
    Exists,
    OuterRef,
    Prefetch,
    Subquery
)
from django_filters.rest_framework import DjangoFilterBackend

# Third Party
from drf_yasg.utils import swagger_auto_schema

# DRF
from rest_framework.filters import OrderingFilter

# Serializers
from community.apps.comments.api.serializers import ParentCommentListSerializer

# Models
from community.apps.comments.models import Comment
from community.apps.emojis.models import CommentEmoji
from community.apps.likes.models import CommentLike, CommentDislike
from community.apps.reports.models import Report

# Bases
from community.bases.api import mixins
from community.bases.api.viewsets import GenericViewSet

# Utils
from community.utils.decorators import swagger_decorator


# Main Section
class CommentsViewSet(mixins.ListModelMixin, GenericViewSet):
    serializers = {"default": ParentCommentListSerializer}
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ["point", "created"]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return None

        user = self.request.user
        comment_emoji_Prefetch = CommentEmoji.objects.get_comment_emojis_prefetch(user)
        queryset = (
            Comment.active.filter(post=self.kwargs["post_pk"])
            .select_related(
                "community",
                "user",
                "user__badge",
                "post",
            )
            .prefetch_related(
                Prefetch(
                    "comments",
                    queryset=Comment.available.select_related(
                        "community",
                        "user",
                        "user__badge",
                        "post",
                    ).prefetch_related(comment_emoji_Prefetch),
                    to_attr="child_comments",
                ),
                comment_emoji_Prefetch,
            )
        )

        if user and user.is_authenticated:
            is_liked_subquery = CommentLike.available.filter(comment=OuterRef("pk"), user=user).values("id")
            is_disliked_subquery = CommentDislike.available.filter(comment=OuterRef("pk"), user=user).values("id")
            is_reported_subquery = Report.available.filter(comment=OuterRef("pk"), user=user).values("id")

            queryset = queryset.annotate(
                is_liked=Exists(Subquery(is_liked_subquery)),
                is_disliked=Exists(Subquery(is_disliked_subquery)),
                is_reported=Exists(Subquery(is_reported_subquery)),
            )

        return queryset

    @swagger_auto_schema(
        **swagger_decorator(
            tag="03. 포스트",
            id="댓글 리스트 조회",
            description="## < 댓글 리스트 조회 API 입니다. >\n" "### ordering : `point (포인트순)`, `created (생성순)` \n",
            response={200: ParentCommentListSerializer},
        )
    )
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)
