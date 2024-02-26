from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PostTagsConfig(AppConfig):
    name = 'community.apps.post_tags'
    verbose_name = _('Post Tag')

    def ready(self):
        import community.apps.post_tags.signals
