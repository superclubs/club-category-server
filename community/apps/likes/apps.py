from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LikesConfig(AppConfig):
    name = 'community.apps.likes'
    verbose_name = _('Like')

    def ready(self):
        import community.apps.likes.signals
