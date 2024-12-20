# Django
from django.utils.translation import gettext_lazy as _

# Third Party
from model_utils import Choices

USER_TYPE_CHOICES = Choices(
    (0, _("GUEST")),
    (1, _("FARMER")),
    (2, _("KNIGHT")),
    (3, _("VISCOUNT")),
    (4, _("EARL")),
    (5, _("DUKE")),
    (6, _("KING")),
    (7, _("STAFF")),
    (8, _("PRO_STAFF")),
    (9, _("SUPER_STAFF")),
    (10, _("MASTER")),
)

USER_STATUS_CHOICES = Choices(
    ("ACTIVE", _("ACTIVE")),
    ("DEACTIVE", _("DEACTIVE")),
    ("WITHDRAWING", _("WITHDRAWING")),
    ("WITHDRAWN", _("WITHDRAWN")),
)

VIEW_MODE_CHOICES = Choices(
    ("LIST_TYPE", _("LIST_TYPE")),
    ("ALBUM_TYPE", _("ALBUM_TYPE")),
    ("CARD_TYPE", _("CARD_TYPE")),
)

LINK_SHARE_CHOICES = Choices(
    ("LINK", _("LINK")),
    ("TWITTER", _("TWITTER")),
    ("FACEBOOK", _("FACEBOOK")),
    ("TELEGRAM", _("TELEGRAM")),
)

BOARD_GROUP_TYPE_CHOICES = Choices(
    ("NORMAL", _("NORMAL")),
    ("DEFAULT", _("DEFAULT")),
)

BOARD_TYPE_CHOICES = Choices(
    ("NORMAL", _("NORMAL")),
    ("ALL", _("ALL")),
    ("NOTICE", _("NOTICE")),
    ("EVENT", _("EVENT")),
    ("GALLERY", _("GALLERY")),
    ("VIDEO", _("VIDEO")),
)

ORDER_TYPE_CHOICES = Choices(
    ("CREATED", _("생성순")),
    ("ORDER", _("오더순")),
)

LIKE_TYPE_CHOICES = Choices(
    ("LIKE", _("LIKE")),
    ("FUN", _("FUN")),
    ("HEALING", _("HEALING")),
    ("LEGEND", _("LEGEND")),
    ("USEFUL", _("USEFUL")),
    ("EMPATHY", _("EMPATHY")),
    ("DEVIL", _("DEVIL")),
)

MODEL_TYPE_CHOICES = Choices(
    ("POST", _("포스트")),
)

RANKING_TYPE_CHOICES = Choices(
    ("LIVE", _("LIVE")),
    ("WEEKLY", _("WEEKLY")),
    ("MONTHLY", _("MONTHLY")),
    ("RISING", _("RISING")),
)

PUBLIC_TYPE_CHOICES = Choices(
    ("PUBLIC", _("PUBLIC")),
    ("FRIEND", _("FRIEND")),
    ("ONLY_ME", _("ONLY_ME")),
)

BOOM_PERIOD_CHOICES = Choices(
    ("5", "5m"),
    ("30", "30m"),
    ("60", "1h"),
    ("360", "6h"),
    ("1440", "1d"),
    ("10080", "7d"),
)

COMMUNITY_MEDIA_TYPE_CHOICES = Choices(
    ("BANNER", _("BANNER")),
)

FILE_TYPE_CHOICES = Choices(
    ("IMAGE", _("IMAGE")),
    ("VIDEO", _("VIDEO")),
)

BADGE_TYPE_CHOICES = Choices(
    ("POST_ACTIVE", _("포스트 활성화")),
    ("POST_PERIOD", _("포스트 기간")),
)

ICON_TYPE = Choices(
    ("BADGE", _("BADGE")),
    ("PROFILE_BADGE", _("PROFILE_BADGE")),
    ("LABEL", _("LABEL")),
    ("USER_INFO", _("USER_INFO")),
)

FRIEND_REQUEST_AVAILABLE_STATUS = Choices(
    ("SEND", _("SEND")),
    ("RECEIVED", _("RECEIVED")),
    ("APPROVED", _("APPROVED")),
    ("UNAVAILABLE", _("UNAVAILABLE")),
    ("BANNED", _("BANNED")),
)
