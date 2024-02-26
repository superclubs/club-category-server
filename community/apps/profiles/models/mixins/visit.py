# Python
import math

# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Utils
from community.utils.point import POINT_PER_COMMUNITY_VISIT, POINT_PER_PROFILE_LEVEL


# Main Section
class ProfileVisitModelMixin(models.Model):
    community_visit_count = models.IntegerField(_('Club Visit Count'), default=0)

    class Meta:
        abstract = True

    def increase_community_visit_count(self):
        self.community_visit_count = self.community_visit_count + 1

        # Point
        self.community_visit_point = self.community_visit_point + POINT_PER_COMMUNITY_VISIT
        self.point = self.point + POINT_PER_COMMUNITY_VISIT

        self.level = math.floor(self.point ** POINT_PER_PROFILE_LEVEL) + 1

    def update_community_visit_count(self):
        self.community_visit_count = self.community_visits.filter(is_active=True, is_deleted=False).count()
