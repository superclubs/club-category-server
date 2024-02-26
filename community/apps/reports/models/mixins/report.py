# Django
from django.db import models
from django.utils.translation import gettext_lazy as _


# Main Section
class ReportGroupReportModelMixin(models.Model):
    reported_count = models.IntegerField(_('Reported Count'), default=0)

    class Meta:
        abstract = True

    def increase_report_group_reported_count(self):
        self.reported_count = self.reported_count + 1

    def decrease_report_group_reported_count(self):
        self.reported_count = self.reported_count - 1

    def update_report_group_reported_count(self):
        self.reported_count = self.reports.filter(is_active=True, is_deleted=False).count()
