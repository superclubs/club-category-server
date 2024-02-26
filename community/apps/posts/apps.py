from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PostsConfig(AppConfig):
    name = 'community.apps.posts'
    verbose_name = _('Post')

    def ready(self):
        import community.apps.posts.signals
