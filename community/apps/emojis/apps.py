from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class EmojisConfig(AppConfig):
    name = "community.apps.emojis"
    verbose_name = _("Emoji")

    def ready(self):
        import community.apps.emojis.signals.comment
        import community.apps.emojis.signals.post
