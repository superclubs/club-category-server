# Django
from django.db import models
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _

# Utils
from community.utils.point import POINT_PER_COMMENT


# Main Section
class PostCommentModelMixin(models.Model):
    comment_count = models.IntegerField(_('Comment Count'), default=0)
    comments_like_count = models.IntegerField(_('Comments Like Count'), default=0)
    comments_dislike_count = models.IntegerField(_('Comments Dislike Count'), default=0)

    class Meta:
        abstract = True

    def increase_post_comment_count(self):
        self.comment_count = self.comment_count + 1

        # Point
        self.comment_point = self.comment_point + POINT_PER_COMMENT
        self.point = self.point + POINT_PER_COMMENT

    def decrease_post_comment_count(self):
        self.comment_count = self.comment_count - 1

        # Point
        self.comment_point = self.comment_point - POINT_PER_COMMENT
        self.point = self.point - POINT_PER_COMMENT

    def increase_post_comments_like_count(self):
        self.comments_like_count = self.comments_like_count + 1

    def decrease_post_comments_like_count(self):
        self.comments_like_count = self.comments_like_count - 1

    def increase_post_comments_dislike_count(self):
        self.comments_dislike_count = self.comments_dislike_count + 1

    def decrease_post_comments_dislike_count(self):
        self.comments_dislike_count = self.comments_dislike_count - 1

    def update_post_comment_count(self):
        self.comment_count = self.comments.filter(is_active=True, is_deleted=False).count()

    def update_post_comments_like_count(self):
        self.comments_like_count = \
            self.comments.filter(is_active=True, is_deleted=False).aggregate(Sum('like_count'))['like_count__sum']

    def update_post_comments_dislike_count(self):
        self.comments_dislike_count = \
            self.comments.filter(is_active=True, is_deleted=False).aggregate(Sum('dislike_count'))['dislike_count__sum']
