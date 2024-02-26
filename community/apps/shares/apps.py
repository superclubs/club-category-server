from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SharesConfig(AppConfig):
    name = 'community.apps.shares'
    verbose_name = _('Share')
