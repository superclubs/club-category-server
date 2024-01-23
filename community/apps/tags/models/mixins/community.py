# Django
from django.db import models
from django.utils.translation import gettext_lazy as _


# Main Section
class TagCommunityModelMixin(models.Model):
    community_count = models.IntegerField(_('Community Count'), default=0)

    class Meta:
        abstract = True

    def increase_tag_community_count(self):
        self.community_count = self.community_count + 1

    def decrease_tag_community_count(self):
        self.community_count = self.community_count - 1

    def update_tag_community_count(self):
        self.community_count = self.community_count.filter(is_active=True, is_deleted=False).count()
