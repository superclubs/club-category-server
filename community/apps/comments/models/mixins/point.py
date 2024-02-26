# Django
from django.db import models
from django.utils.translation import gettext_lazy as _


# Main Section
class CommentPointModelMixin(models.Model):
    point = models.IntegerField(_('Point'), default=0)

    class Meta:
        abstract = True

    def increase_comment_point(self):
        self.point = self.point + 3

    def decrease_comment_point(self):
        self.point = self.point - 3

    def update_comment_point(self):
        like_point = self.comment_likes.filter(is_active=True, is_deleted=False).count() * 3
        self.point = like_point
