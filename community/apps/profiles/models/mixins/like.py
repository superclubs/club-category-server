# Python
import math

# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Utils
from community.utils.point import POINT_PER_POST_LIKE, POINT_PER_PROFILE_LEVEL, POINT_PER_POST_DISLIKE, \
    POINT_PER_COMMENT_LIKE, POINT_PER_COMMENT_DISLIKE


# Main Section
class ProfileLikeModelMixin(models.Model):
    posts_like_count = models.IntegerField(_('Posts Like Count'), default=0)
    posts_dislike_count = models.IntegerField(_('Posts Dislike Count'), default=0)
    comments_like_count = models.IntegerField(_('Comment Like Count'), default=0)
    comments_dislike_count = models.IntegerField(_('Comment DisLike Count'), default=0)

    class Meta:
        abstract = True

    def increase_profile_posts_like_count(self):
        self.posts_like_count = self.posts_like_count + 1

        # Point
        self.posts_like_point = self.posts_like_point + POINT_PER_POST_LIKE
        self.point = self.point + POINT_PER_POST_LIKE

        self.level = math.floor(self.point ** POINT_PER_PROFILE_LEVEL) + 1

    def decrease_profile_posts_like_count(self):
        self.posts_like_count = self.posts_like_count - 1

        # Point
        self.posts_like_point = self.posts_like_point - POINT_PER_POST_LIKE
        self.point = self.point - POINT_PER_POST_LIKE

        self.level = math.floor(self.point ** POINT_PER_PROFILE_LEVEL) + 1

    def increase_profile_posts_dislike_count(self):
        self.posts_dislike_count = self.posts_dislike_count + 1

        # Point
        self.posts_dislike_point = self.posts_dislike_point + POINT_PER_POST_DISLIKE
        self.point = self.point + POINT_PER_POST_DISLIKE

        self.level = math.floor(self.point ** POINT_PER_PROFILE_LEVEL) + 1

    def decrease_profile_posts_dislike_count(self):
        self.posts_dislike_count = self.posts_dislike_count - 1

        # Point
        self.posts_dislike_point = self.posts_dislike_point - POINT_PER_POST_DISLIKE
        self.point = self.point - POINT_PER_POST_DISLIKE

        self.level = math.floor(self.point ** POINT_PER_PROFILE_LEVEL) + 1

    def increase_profile_comments_like_count(self):
        self.comments_like_count = self.comments_like_count + 1

        # Point
        self.comments_like_point = self.comments_like_point + POINT_PER_COMMENT_LIKE
        self.point = self.point + POINT_PER_COMMENT_LIKE

        self.level = math.floor(self.point ** POINT_PER_PROFILE_LEVEL) + 1

    def decrease_profile_comments_like_count(self):
        self.comments_like_count = self.comments_like_count - 1

        # Point
        self.comments_like_point = self.comments_like_point - POINT_PER_COMMENT_LIKE
        self.point = self.point - POINT_PER_COMMENT_LIKE

        self.level = math.floor(self.point ** POINT_PER_PROFILE_LEVEL) + 1

    def increase_profile_comments_dislike_count(self):
        self.comments_dislike_count = self.comments_dislike_count + 1

        # Point
        self.comments_dislike_point = self.comments_dislike_point + POINT_PER_COMMENT_DISLIKE
        self.point = self.point + POINT_PER_COMMENT_DISLIKE

        self.level = math.floor(self.point ** POINT_PER_PROFILE_LEVEL) + 1

    def decrease_profile_comments_dislike_count(self):
        self.comments_dislike_count = self.comments_dislike_count - 1

        # Point
        self.comments_dislike_point = self.comments_dislike_point - POINT_PER_COMMENT_DISLIKE
        self.point = self.point - POINT_PER_COMMENT_DISLIKE

        self.level = math.floor(self.point ** POINT_PER_PROFILE_LEVEL) + 1

    def update_profile_post_like_count(self):
        self.post_like_count = self.post_likes.filter(is_active=True, is_deleted=False).count()

    def update_profile_post_dislike_count(self):
        self.post_dislike_count = self.post_dislikes.filter(is_active=True, is_deleted=False).count()

    def update_profile_comment_total_like_count(self):
        self.total_like_count = self.comment_likes.filter(is_active=True, is_deleted=False).count()

    def update_profile_comment_dislike_count(self):
        self.dislike_count = self.comment_dislikes.filter(is_active=True, is_deleted=False).count()

