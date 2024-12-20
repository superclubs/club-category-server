from django.db import models
from django.utils.translation import gettext_lazy as _

from community.apps.emojis.models.managers import CommentEmojiManager
from community.bases.models import Model


# Main Section
class CommentEmoji(Model):
    comment = models.ForeignKey(
        "comments.Comment", verbose_name=_("Comment"), on_delete=models.CASCADE, related_name="comment_emojis"
    )
    user = models.ForeignKey(
        "users.User", verbose_name=_("User"), on_delete=models.CASCADE, related_name="comment_emojis"
    )
    profile = models.ForeignKey(
        "profiles.Profile", verbose_name=_("Profile"), on_delete=models.CASCADE, related_name="comment_emojis"
    )
    emoji_code = models.CharField(_("Emoji Code"), max_length=255)

    objects = CommentEmojiManager()

    class Meta:
        verbose_name = verbose_name_plural = _("Comment Emoji")
        ordering = ["-created"]
