# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# DRF
from rest_framework.exceptions import ParseError

# Models
from community.apps.reports.models import Report, ReportGroup


# Main Section
class CommentReportModelMixin(models.Model):
    reported_count = models.IntegerField(_('Reported Count'), default=0)

    class Meta:
        abstract = True

    def increase_comment_reported_count(self):
        self.reported_count = self.reported_count + 1

    def decrease_comment_reported_count(self):
        self.reported_count = self.reported_count - 1

    def update_comment_reported_count(self):
        self.reported_count = self.reports.filter(is_active=True, is_deleted=False).count()

    def report_comment(self, user, data):
        # Create Report Group
        report_group = ReportGroup.available.filter(community=self.community, comment=self, post=self.post, user=self.user,
                                                  profile=self.profile).first()
        if not report_group:
            report_group = ReportGroup.objects.create(community=self.community, comment=self, post=self.post, user=self.user,
                                                      profile=self.profile)

        # Create Report
        report = Report.available.filter(report_group=report_group, comment=self, user=user).first()

        if report:
            raise ParseError('이미 신고한 댓글입니다.')
        else:
            user_profile = self.community.profiles.filter(user=user, is_active=True, is_deleted=False).first()
            report = Report.objects.create(**data, post=self.post, profile=user_profile, report_group=report_group,
                                           comment=self, user=user)

        return report.comment
