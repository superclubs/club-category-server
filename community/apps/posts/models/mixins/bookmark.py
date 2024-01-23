# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# DRF
from rest_framework.exceptions import ParseError

# Models
from community.apps.bookmarks.models import PostBookmark

# Utils
from community.utils.point import POINT_PER_BOOKMARK


# Main Section
class PostBookmarkModelMixin(models.Model):
    bookmark_count = models.IntegerField(_('Bookmark Count'), default=0)

    class Meta:
        abstract = True

    def increase_post_bookmark_count(self):
        self.bookmark_count = self.bookmark_count + 1

        # Point
        self.bookmark_point = self.bookmark_point + POINT_PER_BOOKMARK
        self.point = self.point + POINT_PER_BOOKMARK

    def decrease_post_bookmark_count(self):
        self.bookmark_count = self.bookmark_count - 1

        # Point
        self.bookmark_point = self.bookmark_point - POINT_PER_BOOKMARK
        self.point = self.point - POINT_PER_BOOKMARK

    def update_post_bookmark_count(self):
        self.bookmark_count = self.post_bookmarks.filter(is_active=True, is_deleted=False).count()

    def bookmark_post(self, user):
        post_bookmark, created = PostBookmark.available.get_or_create(user=user, post=self)
        if not created:
            post_bookmark.is_active = True
            post_bookmark.save()
        return post_bookmark

    def unbookmark_post(self, user):
        instance = self.post_bookmarks.filter(user=user, is_active=True, is_deleted=False).first()
        if not instance:
            raise ParseError('북마크 객체가 없습니다.')
        instance.is_active = False
        instance.save()
        return instance
