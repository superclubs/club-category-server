from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CommunitiesConfig(AppConfig):
    name = 'community.apps.communities'
    verbose_name = _('Community')

    def ready(self):
        import community.apps.communities.signals
