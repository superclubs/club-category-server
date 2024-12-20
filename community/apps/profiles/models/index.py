# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Mixins
from community.apps.profiles.models.mixins import (
    ProfileCommentModelMixin,
    ProfileLikeModelMixin,
    ProfilePointModelMixin,
    ProfilePostModelMixin,
    ProfileReportModelMixin,
    ProfileVisitModelMixin,
    ProfileEmojiModelMixin,
)

# Bases
from community.bases.models import Model


# Main Section
class Profile(
    ProfileCommentModelMixin,
    ProfilePostModelMixin,
    ProfileVisitModelMixin,
    ProfileReportModelMixin,
    ProfileLikeModelMixin,
    ProfilePointModelMixin,
    ProfileEmojiModelMixin,
    Model,
):
    community = models.ForeignKey(
        "communities.Community", verbose_name=_("Community"), on_delete=models.CASCADE, related_name="profiles"
    )
    user = models.ForeignKey("users.User", verbose_name=_("User"), on_delete=models.CASCADE, related_name="profiles")
    user_data = models.JSONField(_("User Data"), null=True, blank=True)
    username = models.CharField(_("Username"), max_length=100, null=True, blank=True)

    level = models.IntegerField(_("Level"), default=1)
    last_visit = models.DateTimeField(_("Last Visit"), null=True, blank=True)

    class Meta:
        verbose_name = verbose_name_plural = _("Profile")
        unique_together = ("community", "user")
        ordering = ["-created"]

    def save(self, *args, **kwargs):
        if self.id is None:
            self.username = self.user.username
        return super(Profile, self).save(*args, **kwargs)
