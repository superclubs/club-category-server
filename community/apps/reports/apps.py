from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ReportsConfig(AppConfig):
    name = 'community.apps.reports'
    verbose_name = _('Report')

    def ready(self):
        import community.apps.reports.signals
