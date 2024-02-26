# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Django Rest Framework
from rest_framework.exceptions import ParseError

# Models
from community.apps.reports.models import Report, ReportGroup


# Main Section
class PostReportModelMixin(models.Model):
    reported_count = models.IntegerField(_('Reported Count'), default=0)

    class Meta:
        abstract = True

    def increase_post_reported_count(self):
        self.reported_count = self.reported_count + 1

    def decrease_post_reported_count(self):
        self.reported_count = self.reported_count - 1

    def update_post_reported_count(self):
        self.reported_count = self.reports.filter(is_active=True, is_deleted=False).count()

    def report_post(self, user, data):
        # Create Report Group
        report_group = ReportGroup.available.filter(community=self.community, post=self, user=self.user,
                                                  profile=self.profile).first()

        if not report_group:
            report_group = ReportGroup.objects.create(community=self.community, post=self, user=self.user,
                                                      profile=self.profile)

        reporter = self.user.profiles.filter(community=self.community, is_joined=True, is_active=True, is_deleted=False).first()
        report = Report.available.filter(report_group=report_group, post=self, user=user, profile=reporter).first()

        if report:
            raise ParseError('이미 신고한 포스트입니다.')
        else:
            report = Report.objects.create(**data, report_group=report_group, post=self, user=user, profile=reporter)

        return report.post
