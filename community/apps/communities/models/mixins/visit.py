# Python
import math
from dateutil.relativedelta import relativedelta

# Django
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

# Models
from community.apps.visits.models import CommunityVisit

# Utils
from community.utils.point import POINT_PER_POST_VISIT, POINT_PER_COMMUNITY_LEVEL


# Main Section
class CommunityVisitModelMixin(models.Model):
    visit_count = models.IntegerField(_('Visit Count'), default=0)

    class Meta:
        abstract = True

    def increase_community_visit_count(self):
        self.visit_count = self.visit_count + 1

    def update_community_visit_count(self):
        self.visit_count = self.community_visits.filter(is_active=True, is_deleted=False).count()

    # TODO: 프로필 비 활성화 or 밴 기획이 생기면 로직 변경 필요
    def create_community_visit(self, profile):
        if not profile:
            return

        community_visit = CommunityVisit.available.filter(profile=profile, community=self).first()

        if not community_visit:
            CommunityVisit.objects.create(profile=profile, community=self)

        else:
            if community_visit and now() > community_visit.created + relativedelta(hours=3):
                CommunityVisit.objects.create(profile=profile, community=self)

            else:
                community_visit.last_seen = now()
                community_visit.save(update_fields=['last_seen'])


class CommunityPostVisitModelMixin(models.Model):
    posts_visit_count = models.IntegerField(_('Posts Visit Count'), default=0)

    class Meta:
        abstract = True

    def increase_community_posts_visit_count(self):
        self.posts_visit_count = self.posts_visit_count + 1

        # Point
        self.posts_visit_point = self.posts_visit_point + POINT_PER_POST_VISIT
        self.point = self.point + POINT_PER_POST_VISIT

        self.level = math.floor(self.point ** POINT_PER_COMMUNITY_LEVEL) + 1
