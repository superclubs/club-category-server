from django.db import models
from django.utils.translation import gettext_lazy as _

from community.apps.emojis.models.managers import PostEmojiManager
from community.bases.models import Model


# Main Section
class PostEmoji(Model):
    post = models.ForeignKey("posts.Post", verbose_name=_("Post"), on_delete=models.CASCADE, related_name="post_emojis")
    user = models.ForeignKey("users.User", verbose_name=_("User"), on_delete=models.CASCADE, related_name="post_emojis")
    profile = models.ForeignKey(
        "profiles.Profile", verbose_name=_("Profile"), on_delete=models.CASCADE, related_name="post_emojis"
    )
    emoji_code = models.CharField(_("Emoji Code"), max_length=255)

    objects = PostEmojiManager()

    class Meta:
        verbose_name = verbose_name_plural = _("Post Emoji")
        ordering = ["-created"]
