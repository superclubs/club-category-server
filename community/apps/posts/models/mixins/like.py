# Python
import random

# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Django Rest Framework
from rest_framework.exceptions import ParseError

# Models
from community.apps.likes.models import PostLike, PostDislike
from community.apps.users.models import User
from community.apps.profiles.models import Profile

# Utils
from community.utils.point import POINT_PER_POST_LIKE, POINT_PER_POST_DISLIKE


# Main Section
class PostLikeModelMixin(models.Model):
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

    def increase_post_total_like_count(self):
        self.total_like_count = self.total_like_count + 1

        # Point
        self.like_point = self.like_point + POINT_PER_POST_LIKE
        self.point = self.point + POINT_PER_POST_LIKE

    def decrease_post_total_like_count(self):
        self.total_like_count = self.total_like_count - 1

        # Point
        self.like_point = self.like_point - POINT_PER_POST_LIKE
        self.point = self.point - POINT_PER_POST_LIKE

    def increase_post_dislike_count(self):
        self.dislike_count = self.dislike_count + 1

        # Point
        self.dislike_point = self.dislike_point + POINT_PER_POST_DISLIKE
        self.point = self.point + POINT_PER_POST_DISLIKE

    def decrease_post_dislike_count(self):
        self.dislike_count = self.dislike_count - 1

        # Point
        self.dislike_point = self.dislike_point - POINT_PER_POST_DISLIKE
        self.point = self.point - POINT_PER_POST_DISLIKE

    def increase_post_like_count(self):
        self.like_count = self.like_count + 1

    def decrease_post_like_count(self):
        self.like_count = self.like_count - 1

    def increase_post_fun_count(self):
        self.fun_count = self.fun_count + 1

    def decrease_post_fun_count(self):
        self.fun_count = self.fun_count - 1

    def increase_post_healing_count(self):
        self.healing_count = self.healing_count + 1

    def decrease_post_healing_count(self):
        self.healing_count = self.healing_count - 1

    def increase_post_legend_count(self):
        self.legend_count = self.legend_count + 1

    def decrease_post_legend_count(self):
        self.legend_count = self.legend_count - 1

    def increase_post_useful_count(self):
        self.useful_count = self.useful_count + 1

    def decrease_post_useful_count(self):
        self.useful_count = self.useful_count - 1

    def increase_post_empathy_count(self):
        self.empathy_count = self.empathy_count + 1

    def decrease_post_empathy_count(self):
        self.empathy_count = self.empathy_count - 1

    def increase_post_devil_count(self):
        self.devil_count = self.devil_count + 1

    def decrease_post_devil_count(self):
        self.devil_count = self.devil_count - 1

    def update_post_total_like_count(self):
        self.total_like_count = self.post_likes.filter(is_active=True, is_deleted=False).count()

    def update_post_like_count(self):
        self.like_count = self.post_likes.filter(is_active=True, type='LIKE').count()

    def update_post_fun_count(self):
        self.fun_count = self.post_likes.filter(is_active=True, type='FUN').count()

    def update_post_healing_count(self):
        self.healing_count = self.post_likes.filter(is_active=True, type='HEALING').count()

    def update_post_legend_count(self):
        self.legend_count = self.post_likes.filter(is_active=True, type='LEGEND').count()

    def update_post_useful_count(self):
        self.useful_count = self.post_likes.filter(is_active=True, type='USEFUL').count()

    def update_post_empathy_count(self):
        self.empathy_count = self.post_likes.filter(is_active=True, type='EMPATHY').count()

    def update_post_devil_count(self):
        self.devil_count = self.post_likes.filter(is_active=True, type='DEVIL').count()

    def update_post_dislike_count(self):
        self.dislike_count = self.post_dislikes.filter(is_active=True, is_deleted=False).count()

    def like_post(self, user, like_type):
        profile = self.community.profiles.filter(user=user).first()

        if self.community and not profile:
            profile = Profile.objects.create(community=self.community, user=user, is_joined=False)

        post_dislike = self.post_dislikes.filter(user=user).first()
        if post_dislike:
            post_dislike.is_active = False
            post_dislike.save()

        if post_like := self.post_likes.filter(user=user).first():
            post_like.is_active = True
            post_like.type = like_type
            post_like.save(update_fields=['is_active', 'type'])
        else:
            post_like = PostLike.objects.create(user=user, post=self, profile=profile, community=self.community, type=like_type)

        return post_like.post

    def unlike_post(self, user):
        instance = self.post_likes.filter(user=user, is_active=True).first()
        if not instance:
            raise ParseError('좋아요 객체가 없습니다.')
        instance.is_active = False
        instance.save()

        return instance.post

    def dislike_post(self, user):
        profile = self.community.profiles.filter(user=user).first()

        if self.community and not profile:
            profile = Profile.objects.create(community=self.community, user=user, is_joined=False)

        post_like = self.post_likes.filter(user=user).first()
        if post_like:
            post_like.is_active = False
            post_like.save()

        post_dislike, created = PostDislike.objects.get_or_create(user=user, post=self, profile=profile, community=self.community)
        if not created:
            post_dislike.is_active = True
            post_dislike.save()

        return post_dislike.post

    def undislike_post(self, user):
        instance = self.post_dislikes.filter(user=user, is_active=True).first()
        if not instance:
            raise ParseError('싫어요 객체가 없습니다.')
        instance.is_active = False
        instance.save()

        return instance.post

    # Admin Site Inline Action
    def create_post_like(self):
        self.post_likes.all().delete()

        max_num = User.available.all().count()
        random_num = random.randint(1, max_num)
        users = User.available.filter(id__gte=random_num)

        type_list = ['LIKE', 'FUN', 'HEALING', 'LEGEND', 'USEFUL', 'EMPATHY', 'DEVIL']

        for user in users:

            post_dislike = self.post_dislikes.filter(user=user).first()
            if post_dislike:
                post_dislike.is_active = False
                post_dislike.save()

            random_type = random.choice(type_list)
            profile = self.community.profiles.filter(user=user).first()
            PostLike.objects.create(user=user, post=self, profile=profile, type=random_type)

    def create_post_dislike(self):
        self.post_dislikes.all().delete()
        max_num = User.available.all().count()
        random_num = random.randint(1, max_num)
        users = User.available.filter(id__gte=random_num)
        for user in users:

            post_like = self.post_likes.filter(user=user).first()
            if post_like:
                post_like.is_active = False
                post_like.save()

            profile = self.community.profiles.filter(user=user).first()
            PostDislike.objects.create(user=user, post=self, profile=profile)
