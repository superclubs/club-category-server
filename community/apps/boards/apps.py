from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BoardsConfig(AppConfig):
    name = 'community.apps.boards'
    verbose_name = _('Board')

    def ready(self):
        import community.apps.boards.signals
