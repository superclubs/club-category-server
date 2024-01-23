# Django
from django.db import models
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _


# Main Section
class BoardCommentModelMixin(models.Model):
    comment_count = models.IntegerField(_('Comment Count'), default=0)

    class Meta:
        abstract = True

    def increase_board_comment_count(self):
        self.comment_count = self.comment_count + 1

    def decrease_board_comment_count(self):
        self.comment_count = self.comment_count - 1

    def update_board_comment_count(self):
        # Get Active Posts
        posts = self.posts.filter(is_active=True, is_deleted=False, is_temporary=False)

        total_comment_count = posts.aggregate(total=Sum('comment_count'))['total']
        if total_comment_count is None:
            total_comment_count = 0

        self.comment_count = total_comment_count
