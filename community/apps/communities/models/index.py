# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Mixins
from community.apps.communities.models.mixins import CommunityBoardGroupModelMixin, CommunityCommentModelMixin,\
    CommunityImageModelMixin, CommunityPointModelMixin, CommunityPostModelMixin, CommunityRankModelMixin, \
    CommunityVisitModelMixin, CommunityPostVisitModelMixin, CommunityLikeModelMixin

# Bases
from community.bases.models import Model


# Main Section
class Community(CommunityPostModelMixin,
                CommunityVisitModelMixin,
                CommunityCommentModelMixin,
                CommunityImageModelMixin,
                CommunityBoardGroupModelMixin,
                CommunityRankModelMixin,
                CommunityPostVisitModelMixin,
                CommunityLikeModelMixin,
                CommunityPointModelMixin,
                Model):
    # Fk
    parent_community = models.ForeignKey('self', verbose_name=_('Parent Community'), on_delete=models.SET_NULL,
                                         null=True, blank=True, related_name='communities')
    user = models.ForeignKey('users.User', verbose_name=_('Master'), on_delete=models.SET_NULL, null=True,
                             related_name='communities')

    # Main
    title = models.CharField(_('Title'), max_length=30)
    description = models.CharField(_('Description'), max_length=200, null=True, blank=True)
    address = models.CharField(_('Address'), max_length=20)
    level = models.IntegerField(_('Level'), default=1)

    # Data
    user_data = models.JSONField(_('Master Data'), null=True, blank=True)
    profile_data = models.JSONField(_('Master Profile Data'), null=True, blank=True)
    board_data = models.JSONField(_('Board Data'), null=True, blank=True)

    class Meta:
        verbose_name = verbose_name_plural = _('Community')
        ordering = ['-created']

    def __str__(self):
        return f'{self.id} | {self.title}'
