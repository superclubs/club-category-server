# Django
from django.db import models
from django.utils.translation import gettext_lazy as _


# Main Section
class ProfilePointModelMixin(models.Model):
    point = models.IntegerField(_("Point"), default=0)

    posts_emoji_point = models.IntegerField(_("Posts Emoji Point"), default=0)
    comments_emoji_point = models.IntegerField(_("Comments Emoji Point"), default=0)

    community_visit_point = models.IntegerField(_("Community Visit Point"), default=0)
    post_point = models.IntegerField(_("Post Point"), default=0)
    posts_like_point = models.IntegerField(_("Posts Like Point"), default=0)
    posts_dislike_point = models.IntegerField(_("Posts Dislike Point"), default=0)
    comment_point = models.IntegerField(_("Comment Point"), default=0)
    comments_like_point = models.IntegerField(_("Comments Like Point"), default=0)
    comments_dislike_point = models.IntegerField(_("Comments Dislike Point"), default=0)

    class Meta:
        abstract = True

    def update_profile_point(self):
        self.point = (
            self.post_point
            + self.posts_like_point
            + self.posts_dislike_point
            + self.club_visit_point
            + self.comment_point
            + self.comments_like_point
            + self.comments_dislike_point
            + self.posts_emoji_point
            + self.comments_emoji_point
        )

    def reset_profile_point(self):
        self.point = 0
        self.club_visit_point = 0
        self.post_point = 0
        self.posts_like_point = 0
        self.posts_dislike_point = 0
        self.comment_point = 0
        self.comments_like_point = 0
        self.comments_dislike_point = 0
        self.posts_emoji_point = 0
        self.comments_emoji_point = 0
        self.level = 0
