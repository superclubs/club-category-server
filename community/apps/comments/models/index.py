# Python
import random

# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Managers
from community.apps.comments.models.managers.active import CommentActiveManager
from community.apps.comments.models.managers.objects import CommentMainManager

# Mixins
from community.apps.comments.models.mixins import CommentLikeModelMixin, CommentImageModelMixin, CommentPointModelMixin, \
    CommentReportModelMixin

# Models
from community.apps.likes.models import CommentLike, CommentDislike
from community.apps.users.models import User

# Serializer
from community.apps.profiles.api.serializers import ProfileSerializer
from community.apps.users.api.serializers import UserSerializer

# Bases
from community.bases.models import Model

# Utils
from community.utils.time import get_start_today, get_end_today
from community.utils.point import POINT_PER_PARENT_COMMENT
from community.utils.point_history_type import HISTORY_CREATE_CHILD_COMMENT, HISTORY_CREATE_COMMENT
from community.utils.point import FRIEND_POINT_PER_CREATE_CHILD_COMMENT, FRIEND_POINT_PER_CREATE_COMMENT
from community.utils.fields import extract_content_summary


# Main Section
class Comment(CommentLikeModelMixin,
              CommentImageModelMixin,
              CommentReportModelMixin,
              CommentPointModelMixin,
              Model):
    parent_comment = models.ForeignKey('self', verbose_name=_('Parent Comment'), on_delete=models.SET_NULL,
                                       null=True, blank=True, related_name='comments')
    community = models.ForeignKey('communities.Community', verbose_name=_('Community'), on_delete=models.CASCADE,
                                  related_name='comments')
    post = models.ForeignKey('posts.Post', verbose_name=_('Post'), on_delete=models.SET_NULL, null=True,
                             related_name='comments')
    user = models.ForeignKey('users.User', verbose_name=_('User'), on_delete=models.SET_NULL, null=True,
                             related_name='comments')
    profile = models.ForeignKey('profiles.Profile', verbose_name=_('Profile'), on_delete=models.SET_NULL,
                                null=True, blank=True, related_name='comments')
    user_data = models.JSONField(_('User Data'), null=True, blank=True)
    profile_data = models.JSONField(_('Profile Data'), null=True, blank=True)
    content = models.TextField(_('Content'), null=True, blank=True)
    content_summary = models.TextField(_('Content Summary'), null=True, blank=True)
    is_secret = models.BooleanField(_('Is Secret'), default=False)

    objects = CommentMainManager()
    active = CommentActiveManager()

    class Meta:
        verbose_name = verbose_name_plural = _('Comment')
        ordering = ['created']

    def __str__(self):
        return self.content if len(self.content) < 20 else self.content[:20]

    def save(self, *args, request=None, **kwargs):
        if self.id is None:
            # Content Summary
            if self.content:
                self.content_summary = extract_content_summary(self.content)

            # Set Comment Field
            self.user_data = UserSerializer(instance=self.user).data
            self.profile_data = ProfileSerializer(instance=self.profile).data

            # User Comment Count
            self.user.increase_user_comment_count()
            self.user.save()

            # Post Comment Count
            self.post.increase_post_comment_count()
            self.post.save()

            # Profile Comment Count
            self.profile.increase_profile_comment_count()
            self.profile.save()

            # Community Comment Count
            self.community.increase_community_comment_count()
            self.community.save()

            # Child Comment
            if self.parent_comment:
                self.parent_comment.point = self.parent_comment.point + POINT_PER_PARENT_COMMENT
                self.parent_comment.save()

        return super(Comment, self).save(*args, **kwargs)

    # Django Admin Site Section
    def create_comment_like(self):
        self.comment_likes.all().delete()

        max_num = User.available.all().count()
        random_num = random.randint(1, max_num)
        users = User.available.filter(id__gte=random_num)

        type_list = ['LIKE', 'FUN', 'HEALING', 'LEGEND', 'USEFUL', 'EMPATHY', 'DEVIL']

        for user in users:

            comment_dislike = self.comment_dislikes.filter(user=user, is_active=True, is_deleted=False).first()
            if comment_dislike:
                comment_dislike.is_active = False
                comment_dislike.save()

            random_type = random.choice(type_list)
            profile = self.community.profiles.filter(user=user, is_active=True, is_deleted=False).first()
            CommentLike.objects.create(user=user, comment=self, profile=profile, type=random_type)

    def create_comment_dislike(self):
        self.comment_dislikes.all().delete()

        max_num = User.available.all().count()
        random_num = random.randint(1, max_num)
        users = User.available.filter(id__gte=random_num)

        for user in users:

            comment_like = self.comment_likes.filter(user=user, is_active=True, is_deleted=False).first()
            if comment_like:
                comment_like.is_active = False
                comment_like.save()

            profile = self.community.profiles.filter(user=user, is_active=True, is_deleted=False).first()
            CommentDislike.objects.create(user=user, comment=self, profile=profile)
