# Python
import math

# Django
from django.db import models
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _

# Utils
from community.utils.point import POINT_PER_COMMUNITY_LEVEL, POINT_PER_POST_LIKE, POINT_PER_POST_DISLIKE, \
    POINT_PER_COMMENT_DISLIKE, POINT_PER_COMMENT_LIKE


# Main Section
class CommunityLikeModelMixin(models.Model):
    posts_like_count = models.IntegerField(_('Posts Like Count'), default=0)
    posts_dislike_count = models.IntegerField(_('Posts Dislike Count'), default=0)
    comments_like_count = models.IntegerField(_('Comments Like Count'), default=0)
    comments_dislike_count = models.IntegerField(_('Comments Dislike Count'), default=0)

    class Meta:
        abstract = True

    def increase_community_posts_like_count(self):
        self.posts_like_count = self.posts_like_count + 1

        # Point
        self.posts_like_point = self.posts_like_point + POINT_PER_POST_LIKE
        self.point = self.point + POINT_PER_POST_LIKE

        self.level = math.floor(self.point ** POINT_PER_COMMUNITY_LEVEL) + 1

    def decrease_community_posts_like_count(self):
        self.posts_like_count = self.posts_like_count - 1

        # Point
        self.posts_like_point = self.posts_like_point - POINT_PER_POST_LIKE
        self.point = self.point - POINT_PER_POST_LIKE

        self.level = math.floor(self.point ** POINT_PER_COMMUNITY_LEVEL) + 1

    def increase_community_posts_dislike_count(self):
        self.posts_dislike_count = self.posts_dislike_count + 1

        # Point
        self.posts_dislike_point = self.posts_dislike_point + POINT_PER_POST_DISLIKE
        self.point = self.point + POINT_PER_POST_DISLIKE

        self.level = math.floor(self.point ** POINT_PER_COMMUNITY_LEVEL) + 1

    def decrease_community_posts_dislike_count(self):
        self.posts_dislike_count = self.posts_dislike_count - 1

        # Point
        self.posts_dislike_point = self.posts_dislike_point - POINT_PER_POST_DISLIKE
        self.point = self.point - POINT_PER_POST_DISLIKE

        self.level = math.floor(self.point ** POINT_PER_COMMUNITY_LEVEL) + 1

    def increase_community_comments_like_count(self):
        self.comments_like_count = self.comments_like_count + 1

        # Point
        self.comments_like_point = self.comments_like_point + POINT_PER_COMMENT_LIKE
        self.point = self.point + POINT_PER_COMMENT_LIKE

        self.level = math.floor(self.point ** POINT_PER_COMMUNITY_LEVEL) + 1

    def decrease_community_comments_like_count(self):
        self.comments_like_count = self.comments_like_count - 1

        # Point
        self.comments_like_point = self.comments_like_point - POINT_PER_COMMENT_LIKE
        self.point = self.point - POINT_PER_COMMENT_LIKE

        self.level = math.floor(self.point ** POINT_PER_COMMUNITY_LEVEL) + 1

    def increase_community_comments_dislike_count(self):
        self.comments_dislike_count = self.comments_dislike_count + 1

        # Point
        self.posts_dislike_point = self.posts_dislike_point + POINT_PER_COMMENT_DISLIKE
        self.point = self.point + POINT_PER_COMMENT_DISLIKE

        self.level = math.floor(self.point ** POINT_PER_COMMUNITY_LEVEL) + 1

    def decrease_community_comments_dislike_count(self):
        self.comments_dislike_count = self.comments_dislike_count - 1

        # Point
        self.comments_dislike_point = self.comments_dislike_point - POINT_PER_COMMENT_DISLIKE
        self.point = self.point - POINT_PER_COMMENT_DISLIKE

        self.level = math.floor(self.point ** POINT_PER_COMMUNITY_LEVEL) + 1

    def update_posts_like_count(self):
        self.posts_like_count = \
            self.posts.filter(is_active=True, is_deleted=False, is_temporary=False).aggregate(Sum('like_count'))['like_count__sum']

    def update_posts_dislike_count(self):
        self.posts_dislike_count = \
            self.posts.filter(is_active=True, is_deleted=False, is_temporary=False).aggregate(Sum('dislike_count'))['dislike_count__sum']

    # post 별로 comment like 갯수도 가지고 있어야 한다.
    def update_comments_like_count(self):
        self.comments_like_count = \
            self.posts.filter(is_active=True, is_deleted=False).aggregate(Sum('comments_like_count'))['comments_like_count__sum']

    def update_comments_dislike_count(self):
        self.comments_dislike_count = \
            self.posts.filter(is_active=True, is_deleted=False).aggregate(Sum('comments_dislike_count'))['comments_dislike_count__sum']
