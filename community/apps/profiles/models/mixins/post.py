# Python
import math

# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Utils
from community.utils.point import POINT_PER_POST, POINT_PER_PROFILE_LEVEL


# Main Section
class ProfilePostModelMixin(models.Model):
    post_count = models.IntegerField(_('Post Count'), default=0)

    class Meta:
        abstract = True

    def increase_profile_post_count(self):
        self.post_count = self.post_count + 1

        # Point
        self.post_point = self.post_point + POINT_PER_POST
        self.point = self.point + POINT_PER_POST

        self.level = math.floor(self.point ** POINT_PER_PROFILE_LEVEL) + 1

    def decrease_profile_post_count(self):
        self.post_count = self.post_count - 1

        # Point
        self.post_point = self.post_point - POINT_PER_POST
        self.point = self.point - POINT_PER_POST

        self.level = math.floor(self.point ** POINT_PER_PROFILE_LEVEL) + 1

    def update_profile_post_count(self):
        self.post_count = self.posts.filter(is_active=True, is_deleted=False, is_temporary=False).count()
