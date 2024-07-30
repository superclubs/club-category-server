# Django
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

# Fields
from community.apps.users.models.fields.phone_number import CustomPhoneNumberField
# Manager
from community.apps.users.models.managers.objects import UserMainManager
# Mixins
from community.apps.users.models.mixins import (
    UserCommentModelMixin,
    UserFriendModelMixin,
    UserImageModelMixin,
    UserPointModelMixin,
    UserPostBookmarkModelMixin,
    UserPostModelMixin,
    UserSyncModelMixin,
)
# Bases
from community.bases.models import Model
# Modules
from community.modules.choices import USER_STATUS_CHOICES


# Main Section
class User(
    UserImageModelMixin,
    UserPostModelMixin,
    UserCommentModelMixin,
    UserFriendModelMixin,
    UserPostBookmarkModelMixin,
    UserPointModelMixin,
    UserSyncModelMixin,
    AbstractUser,
    Model,
):
    id_creta = models.CharField(_("ID (Creta)"), max_length=255, unique=True, null=True, blank=True)
    is_two_factor = models.BooleanField(_("Is Two Factor (Creta)"), default=False)
    token_creta = models.CharField(_("Token (Creta)"), max_length=512, null=True, blank=True)
    token_creta_expired_at = models.DateTimeField(_("Token Expired At (Creta)"), null=True, blank=True)

    email = models.EmailField(_("Email"), null=True, blank=True)
    username = models.CharField(_("Nickname"), max_length=100, null=True, blank=True)
    phone = CustomPhoneNumberField(_("Phone"), max_length=20, null=True, blank=True)

    level = models.IntegerField(_("Level"), default=1)
    grade_title = models.CharField(_("Grade Title"), max_length=100, default="NOVICE")
    ring_color = models.CharField(_("Ring Color"), max_length=100, default="LITE_GREY")
    badge_image_url = models.URLField(_("Badge Image URL"), null=True, blank=True)
    web_url = models.URLField(_("Web URL"), null=True, blank=True)
    status = models.CharField(_("Status"), choices=USER_STATUS_CHOICES, default="ACTIVE", max_length=20)
    hash = models.CharField(_("Hash"), max_length=10, null=True, blank=True)
    wallet_address = models.CharField(_("Wallet Address"), max_length=255, null=True, blank=True)
    gender = models.CharField(_("Gender"), max_length=20, null=True, blank=True)
    religion = models.CharField(_("Religion"), max_length=40, null=True, blank=True)
    birth = models.DateField(_("Birth"), null=True, blank=True)
    nation = models.CharField(_("Nation"), max_length=255, null=True, blank=True)
    religion = models.CharField(_("Religion"), max_length=40, null=True, blank=True)
    sdk_id = models.IntegerField(_("Sdk Id"), null=True)
    sdk_uuid = models.UUIDField(_("Sdk UUID"), null=True, blank=True)

    # FK
    badge = models.ForeignKey(
        "badges.Badge", verbose_name=_("Badge"), on_delete=models.SET_NULL, null=True, related_name="users"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserMainManager()

    class Meta:
        verbose_name = verbose_name_plural = _("User")
        ordering = ["-created"]

    def __str__(self):
        return f"{self.__class__.__name__}({self.id})"
