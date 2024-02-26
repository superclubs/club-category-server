# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Django Rest Framework
from rest_framework.exceptions import ParseError

# Models
from community.apps.likes.models import CommentDislike, CommentLike
from community.apps.profiles.models import Profile


# Main Section
class CommentLikeModelMixin(models.Model):
    total_like_count = models.IntegerField(_('Total Like Count'), default=0)
    like_count = models.IntegerField(_('Like Count'), default=0)
    fun_count = models.IntegerField(_('Fun Count'), default=0)
    healing_count = models.IntegerField(_('Healing Count'), default=0)
    legend_count = models.IntegerField(_('Legend Count'), default=0)
    useful_count = models.IntegerField(_('Useful Count'), default=0)
    empathy_count = models.IntegerField(_('Empathy Count'), default=0)
    devil_count = models.IntegerField(_('Devil Count'), default=0)
    dislike_count = models.IntegerField(_('Dislike Count'), default=0)

    class Meta:
        abstract = True

    def increase_comment_total_like_count(self):
        self.total_like_count = self.total_like_count + 1

    def decrease_comment_total_like_count(self):
        self.total_like_count = self.total_like_count - 1

    def increase_comment_like_count(self):
        self.like_count = self.like_count + 1

    def decrease_comment_like_count(self):
        self.like_count = self.like_count - 1

    def increase_comment_fun_count(self):
        self.fun_count = self.fun_count + 1

    def decrease_comment_fun_count(self):
        self.fun_count = self.fun_count - 1

    def increase_comment_healing_count(self):
        self.healing_count = self.healing_count + 1

    def decrease_comment_healing_count(self):
        self.healing_count = self.healing_count - 1

    def increase_comment_legend_count(self):
        self.legend_count = self.legend_count + 1

    def decrease_comment_legend_count(self):
        self.legend_count = self.legend_count - 1

    def increase_comment_useful_count(self):
        self.useful_count = self.useful_count + 1

    def decrease_comment_useful_count(self):
        self.useful_count = self.useful_count - 1

    def increase_comment_empathy_count(self):
        self.empathy_count = self.empathy_count + 1

    def decrease_comment_empathy_count(self):
        self.empathy_count = self.empathy_count - 1

    def increase_comment_devil_count(self):
        self.devil_count = self.devil_count + 1

    def decrease_comment_devil_count(self):
        self.devil_count = self.devil_count - 1

    def increase_comment_dislike_count(self):
        self.dislike_count = self.dislike_count + 1

    def decrease_comment_dislike_count(self):
        self.dislike_count = self.dislike_count - 1

    def update_comment_total_like_count(self):
        self.total_like_count = self.comment_likes.filter(is_active=True, is_deleted=False).count()

    def update_comment_like_count(self):
        self.like_count = self.comment_likes.filter(is_active=True, type='LIKE').count()

    def update_comment_fun_count(self):
        self.fun_count = self.comment_likes.filter(is_active=True, type='FUN').count()

    def update_comment_healing_count(self):
        self.healing_count = self.comment_likes.filter(is_active=True, type='HEALING').count()

    def update_comment_legend_count(self):
        self.legend_count = self.comment_likes.filter(is_active=True, type='LEGEND').count()

    def update_comment_useful_count(self):
        self.useful_count = self.comment_likes.filter(is_active=True, type='USEFUL').count()

    def update_comment_empathy_count(self):
        self.empathy_count = self.comment_likes.filter(is_active=True, type='EMPATHY').count()

    def update_comment_devil_count(self):
        self.devil_count = self.comment_likes.filter(is_active=True, type='DEVIL').count()

    def update_comment_dislike_count(self):
        self.dislike_count = self.comment_dislikes.filter(is_active=True, is_deleted=False).count()

    def like_comment(self, user, like_type):
        profile = self.community.profiles.filter(user=user, is_active=True, is_deleted=False).first()

        # 커뮤니티에 엮인 댓글에 좋아요 했을 때 프로필이 없을 경우
        if self.community and not profile:
            profile = Profile.objects.create(community=self.community, user=user)

        # 싫어요 객체 있을 경우 비활성화
        comment_dislike = self.comment_dislikes.filter(profile=profile).first()
        if comment_dislike:
            comment_dislike.is_active = False
            comment_dislike.save()

        if comment_like := self.comment_likes.filter(user=user).first():
            comment_like.is_active = True
            comment_like.type = like_type
            comment_like.save(update_fields=['is_active', 'type'])
        else:
            comment_like = CommentLike.objects.create(user=user, comment=self, profile=profile, type=like_type)

        return comment_like.comment

    def unlike_comment(self, user):
        comment_like = self.comment_likes.filter(user=user, is_active=True).first()
        if not comment_like:
            raise ParseError('활성화된 좋아요 객체가 없습니다.')
        comment_like.is_active = False
        comment_like.save()

        return comment_like.comment

    def dislike_comment(self, user):
        profile = self.community.profiles.filter(user=user, is_active=True, is_deleted=False).first()

        # 커뮤니티에 엮인 포스트을 좋아요 했을 때 프로필이 없을 경우
        if self.community and not profile:
            profile = Profile.objects.create(community=self.community, user=user)

        # 좋아요 객체 있을 경우 비활성화
        comment_like = self.comment_likes.filter(profile=profile).first()
        if comment_like:
            comment_like.is_active = False
            comment_like.save()

        # 싫어요 객체 생성
        comment_dislike, created = CommentDislike.objects.get_or_create(user=user, comment=self, profile=profile)
        if not created:
            comment_dislike.is_active = True
            comment_dislike.save()

        return comment_dislike.comment

    def undislike_comment(self, user):
        instance = self.comment_dislikes.filter(user=user, is_active=True).first()
        if not instance:
            raise ParseError('활성화된 싫어요 객체가 없습니다.')
        instance.is_active = False
        instance.save()

        return instance
