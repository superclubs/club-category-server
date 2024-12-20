# Python
import random
from collections import Counter

# Django
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _

# DRF
from rest_framework.exceptions import ParseError

# Models
from community.apps.likes.models import PostDislike, PostLike
from community.apps.profiles.models import Profile
from community.apps.users.models import User

# Utils
from community.utils.point import POINT_PER_POST_DISLIKE, POINT_PER_POST_LIKE


# Main Section
class PostLikeModelMixin(models.Model):
    total_like_count = models.IntegerField(_("Total Like Count"), default=0)
    like_count = models.IntegerField(_("Like Count"), default=0)
    fun_count = models.IntegerField(_("Fun Count"), default=0)
    healing_count = models.IntegerField(_("Healing Count"), default=0)
    legend_count = models.IntegerField(_("Legend Count"), default=0)
    useful_count = models.IntegerField(_("Useful Count"), default=0)
    empathy_count = models.IntegerField(_("Empathy Count"), default=0)
    devil_count = models.IntegerField(_("Devil Count"), default=0)
    dislike_count = models.IntegerField(_("Dislike Count"), default=0)

    class Meta:
        abstract = True

    def set_point(self):
        self.point = (
            self.dislike_point + self.like_point + self.bookmark_point + self.comment_point + self.visit_point +
            self.emoji_point
        )

    def set_type_count(self):
        like_counts = self.post_likes.filter(is_active=True).values_list("type", flat=True)
        counts_dict = Counter(like_counts)

        for field in ('like', 'fun', 'healing', 'legend', 'useful', 'empathy', 'devil'):
            setattr(self, f"{field}_count", counts_dict.get(field.upper(), 0))

    def update_post_total_like_count(self):
        self.total_like_count = self.post_likes.filter(is_active=True).count()

        # Point
        self.like_point = self.total_like_count * POINT_PER_POST_LIKE
        self.set_point()
        self.set_type_count()
        self.save()

    def update_post_dislike_count(self):
        self.dislike_count = self.post_dislikes.filter(is_active=True).count()

        # Point
        self.dislike_point = self.dislike_count * POINT_PER_POST_DISLIKE
        self.set_point()
        self.set_type_count()
        self.save(update_fields=["dislike_count", "dislike_point", "point"])

    def like_post(self, user, like_type):
        with transaction.atomic():
            profile = self.community.profiles.filter(user=user).first()
            if not profile:
                profile = Profile.objects.create(community=self.community, user=user)

            if post_dislike := self.post_dislikes.filter(user=user).first():
                post_dislike.update(is_active=False)

            post_like, created = PostLike.objects.update_or_create(user=user, post=self, defaults={
                "is_active": True,
                "type": like_type,
                "profile": profile,
                "community": self.community,
            })

            return post_like.post

    def unlike_post(self, user):
        with transaction.atomic():
            if post_like := self.post_likes.filter(user=user, is_active=True).first():
                post_like.update(is_active=False)
                return post_like.post
            else:
                raise ParseError("좋아요 객체가 없습니다.")

    def dislike_post(self, user):
        with transaction.atomic():
            profile, created = self.community.profiles.get_or_create(user=user, defaults={'community': self.community})

            if post_like := self.post_likes.filter(user=user).first():
                post_like.update(is_active=False)

            post_dislike, created = PostDislike.objects.update_or_create(
                user=user, post=self, defaults={
                    "is_active": True,
                    'profile': profile,
                    'community': self.community
                }
            )

            return post_dislike.post

    def undislike_post(self, user):
        with transaction.atomic():
            if post_dislike := self.post_dislikes.filter(user=user, is_active=True).first():
                post_dislike.update(is_active=False)
                return post_dislike.post
            else:
                raise ParseError("싫어요 객체가 없습니다.")

    # Admin Site Inline Action
    def create_post_like(self):
        self.post_likes.all().delete()

        max_num = User.objects.all().count()
        random_num = random.randint(1, max_num)
        users = User.objects.filter(id__gte=random_num)

        type_list = ["LIKE", "FUN", "HEALING", "LEGEND", "USEFUL", "EMPATHY", "DEVIL"]

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
        max_num = User.objects.all().count()
        random_num = random.randint(1, max_num)
        users = User.objects.filter(id__gte=random_num)
        for user in users:

            post_like = self.post_likes.filter(user=user).first()
            if post_like:
                post_like.is_active = False
                post_like.save()

            profile = self.community.profiles.filter(user=user).first()
            PostDislike.objects.create(user=user, post=self, profile=profile)
