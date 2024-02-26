from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RankingsConfig(AppConfig):
    name = 'community.apps.rankings'
    verbose_name = _('Ranking')

    def ready(self):
        import community.apps.rankings.signals
