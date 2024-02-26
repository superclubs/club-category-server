from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProfilesConfig(AppConfig):
    name = 'community.apps.profiles'
    verbose_name = _('Profile')

    def ready(self):
        import community.apps.profiles.signals
