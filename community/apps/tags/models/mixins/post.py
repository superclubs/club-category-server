# Django
from django.db import models
from django.utils.translation import gettext_lazy as _


# Main Section
class TagPostModelMixin(models.Model):
    post_count = models.IntegerField(_('Post Count'), default=0)

    class Meta:
        abstract = True

    def increase_tag_post_count(self):
        self.post_count = self.post_count + 1

    def decrease_tag_post_count(self):
        self.post_count = self.post_count - 1

    def update_tag_post_count(self):
        self.post_count = self.post_tags.filter(is_active=True, is_deleted=False, post__is_temporary=False).count()
