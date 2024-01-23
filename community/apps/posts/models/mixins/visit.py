# Python
from dateutil.relativedelta import relativedelta

# Django
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

# Models
from community.apps.visits.models import PostVisit

# Utils
from community.utils.point import POINT_PER_POST_VISIT


# Main Section
class PostVisitModelMixin(models.Model):
    visit_count = models.IntegerField(_('Visit Count'), default=0)

    class Meta:
        abstract = True

    def increase_post_visit_count(self):
        self.visit_count = self.visit_count + 1

        # Point
        self.visit_point = self.visit_point + POINT_PER_POST_VISIT
        self.point = self.point + POINT_PER_POST_VISIT

    def update_post_visit_count(self):
        self.visit_count = self.post_visits.filter(is_active=True, is_deleted=False).count()

    def create_post_visit(self, user):
        post_visit = PostVisit.available.filter(post=self, user=user).first()

        if not post_visit:
            PostVisit.objects.create(user=user, post=self)
        else:
            if post_visit and now() > post_visit.created + relativedelta(hours=3):
                PostVisit.objects.create(user=user, post=self)
