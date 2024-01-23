# Django
from django.db import models
from django.utils.translation import gettext_lazy as _


# Main Section
class UserPostBookmarkModelMixin(models.Model):
    post_bookmark_count = models.IntegerField(_('Post Bookmark Count'), default=0)

    class Meta:
        abstract = True

    def increase_user_post_bookmark_count(self):
        self.post_bookmark_count = self.post_bookmark_count + 1

    def decrease_user_post_bookmark_count(self):
        self.post_bookmark_count = self.post_bookmark_count - 1

    def update_user_post_bookmark_count(self):
        self.post_bookmark_count = self.post_bookmarks.filter(is_active=True, is_deleted=False).count()
