from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CommentsConfig(AppConfig):
    name = 'community.apps.comments'
    verbose_name = _('Comment')

    def ready(self):
        import community.apps.comments.signals
