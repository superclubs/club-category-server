# Django
import math

from django.db import models
from django.utils.translation import gettext_lazy as _

from community.utils.point import POINT_PER_COMMUNITY_LEVEL, POINT_PER_COMMENT


# Main Section
class CommunityCommentModelMixin(models.Model):
    comment_count = models.IntegerField(_('Comment Count'), default=0)

    class Meta:
        abstract = True

    def increase_community_comment_count(self):
        self.comment_count = self.comment_count + 1

        # Point
        self.comment_point = self.comment_point + POINT_PER_COMMENT
        self.point = self.point + POINT_PER_COMMENT

        self.level = math.floor(self.point ** POINT_PER_COMMUNITY_LEVEL) + 1

    def decrease_community_comment_count(self):
        self.comment_count = self.comment_count - 1

        # Point
        self.comment_point = self.comment_point - POINT_PER_COMMENT
        self.point = self.point - POINT_PER_COMMENT

        self.level = math.floor(self.point ** POINT_PER_COMMUNITY_LEVEL) + 1

    def update_community_comment_count(self):
        self.comment_count = self.comments.filter(is_active=True, is_deleted=False).count()
