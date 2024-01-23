# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Models
from community.apps.reports.models import Report


# Main Section
class ProfileReportModelMixin(models.Model):
    reported_count = models.IntegerField(_('Reported Count'), default=0)

    class Meta:
        abstract = True

    def increase_profile_reported_count(self):
        self.reported_count = self.reported_count + 1

    def decrease_profile_reported_count(self):
        self.reported_count = self.reported_count - 1

    def update_profile_reported_count(self):
        comment_reports = Report.available.filter(is_active=True, is_deleted=False, comment__profile=self).count()
        post_reports = Report.available.filter(is_active=True, is_deleted=False, post__profile=self).count()

        self.reported_count = post_reports + comment_reports
