# Django
from django.db import models
from django.utils.translation import gettext_lazy as _


# Main Section
class BoardPostModelMixin(models.Model):
    post_count = models.IntegerField(_('Post Count'), default=0)

    class Meta:
        abstract = True

    def increase_board_post_count(self):
        self.post_count = self.post_count + 1

    def decrease_board_post_count(self):
        self.post_count = self.post_count - 1

    def update_board_post_count(self):
        self.post_count = self.posts.filter(is_active=True, is_deleted=False, is_temporary=False).count()
