import math

from django.db import models
from django.utils.translation import gettext_lazy as _

from community.utils.point import (
    POINT_PER_COMMENT_LIKE,
    POINT_PER_POST_LIKE,
    POINT_PER_PROFILE_LEVEL,
)


# Main Section
class ProfileEmojiModelMixin(models.Model):
    posts_emoji_count = models.IntegerField(_("Posts Emoji Count"), default=0)  # Profile 의 post emoji 표시 개수
    comments_emoji_count = models.IntegerField(_("Comments Emoji Count"), default=0)  # Profile 의 comment emoji 표시 개수

    class Meta:
        abstract = True

    def add_emoji_point(self):
        self.point += self.posts_emoji_point + self.comments_emoji_point

    def update_profile_posts_emoji_count(self):
        self.posts_emoji_count = self.post_emojis.count()

        # Point
        self.posts_emoji_point = self.posts_emoji_count * POINT_PER_POST_LIKE
        self.add_emoji_point()
        self.level = math.floor(self.point**POINT_PER_PROFILE_LEVEL) + 1
        self.save(update_fields=["posts_emoji_count", "posts_emoji_point", "point", "level"])

    def update_profile_comments_emoji_count(self):
        self.comments_emoji_count = self.comment_emojis.count()

        # Point
        self.comments_emoji_point = self.comments_emoji_count * POINT_PER_COMMENT_LIKE
        self.add_emoji_point()
        self.level = math.floor(self.point**POINT_PER_PROFILE_LEVEL) + 1
        self.save(update_fields=["comments_emoji_count", "comments_emoji_point", "point", "level"])
