from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BookmarksConfig(AppConfig):
    name = 'community.apps.bookmarks'
    verbose_name = _('Bookmark')

