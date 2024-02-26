from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BadgesConfig(AppConfig):
    name = 'community.apps.badges'
    verbose_name = _('Badge')

    def ready(self):
        import community.apps.badges.signals
