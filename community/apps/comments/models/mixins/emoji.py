from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ParseError

from community.apps.emojis.models import CommentEmoji
from community.apps.profiles.models import Profile


# Main Section
class CommentEmojiModelMixin(models.Model):
    emoji_count = models.IntegerField(_("Emoji Count"), default=0)

    class Meta:
        abstract = True

    def emoji_comment(self, user, emoji_unicode):
        community = self.community

        with transaction.atomic():
            # Get or Create profile
            profile = community.profiles.select_for_update().filter(user=user).first()
            if not profile:
                profile = Profile.objects.create(community=community, user=user)

            # Update or create emoji
            comment_emoji, _ = CommentEmoji.objects.update_or_create(
                comment=self,
                user=user,
                profile=profile,
                defaults={
                    "emoji_code": emoji_unicode,
                },
            )
            return comment_emoji

    def unemoji_comment(self, user, emoji_code):
        with transaction.atomic():
            # Find the Emoji
            instance = self.comment_emojis.filter(user=user, emoji_code=emoji_code).first()
            if not instance:
                raise ParseError("No Found CommentEmoji.")

            # Delete CommentEmoji
            instance.delete()
            return instance.comment

    def update_emoji_count(self):
        self.emoji_count = self.comment_emojis.count()
        # self.emoji_point = self.emoji_count * POINT_PER_COMMENT_LIKE
        # self.point += self.emoji_point
        self.save(update_fields=["emoji_count"])
