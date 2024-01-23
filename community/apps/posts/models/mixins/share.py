# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Models
from community.apps.shares.models import PostShare


# Main Section
class PostShareModelMixin(models.Model):
    share_count = models.IntegerField(_('Share Count'), default=0)

    class Meta:
        abstract = True

    def increase_post_share_count(self):
        self.share_count = self.share_count + 1

    def decrease_post_share_count(self):
        self.share_count = self.share_count - 1

    def update_post_share_count(self):
        self.share_count = self.post_shares.filter(is_active=True, is_deleted=False).count()

    def share_post(self, user, link):
        return PostShare.objects.create(user=user, post=self, link=link)
