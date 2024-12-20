from django.db import models, transaction
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ParseError

from community.apps.emojis.models import PostEmoji
from community.apps.profiles.models import Profile
from community.utils.point import POINT_PER_POST_LIKE


# Main Section
class PostEmojiModelMixin(models.Model):
    emoji_count = models.IntegerField(_("Emoji Count"), default=0)

    class Meta:
        abstract = True

    def emoji_post(self, user, emoji_unicode):
        community = self.community

        with transaction.atomic():
            # Get or Create profile
            profile = community.profiles.select_for_update().filter(user=user).first()
            if not profile:
                profile = Profile.objects.create(community=community, user=user)

            # Update or create emoji
            post_emoji, _ = PostEmoji.objects.update_or_create(
                post=self,
                user=user,
                profile=profile,
                defaults={
                    "emoji_code": emoji_unicode,
                },
            )
            return post_emoji

    def unemoji_post(self, user, emoji_code):
        with transaction.atomic():
            # Find the Emoji
            instance = self.post_emojis.filter(user=user, emoji_code=emoji_code).first()
            if not instance:
                raise ParseError("No Found PostEmoji.")

            # Delete PostEmoji
            instance.delete()
            return instance.post

    def update_post_emoji_count(self):
        self.emoji_count = self.post_emojis.count()
        self.emoji_point = self.emoji_count * POINT_PER_POST_LIKE
        self.set_point()
        self.save(update_fields=["emoji_count", "emoji_point", "point"])

    def update_comments_emoji_count(self):
        self.comments_emoji_count = self.comments.filter(is_active=True, is_deleted=False).aggregate(
            Sum("emoji_count")
        )["emoji_count__sum"]
        self.save(update_fields=["comments_emoji_count"])
