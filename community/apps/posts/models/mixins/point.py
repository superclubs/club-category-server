# Django
from django.db import models
from django.utils.translation import gettext_lazy as _


# Main Section
class PostPointModelMixin(models.Model):
    point = models.IntegerField(_("Point"), default=0)
    emoji_point = models.IntegerField(_("Emoji Point"), default=0)
    visit_point = models.IntegerField(_("Visit Point"), default=0)
    comment_point = models.IntegerField(_("Comment Point"), default=0)
    bookmark_point = models.IntegerField(_("Bookmark Point"), default=0)
    like_point = models.IntegerField(_("Like Point"), default=0)
    dislike_point = models.IntegerField(_("Dislike Point"), default=0)

    class Meta:
        abstract = True

    def update_post_point(self):
        self.point = self.visit_point + self.comment_point + self.bookmark_point + self.like_point + self.dislike_point
