# Django
from django.db.models import Q
from django.utils.timezone import now

# Manager
from community.apps.posts.models.managers.objects import PostMainManager


# Main Section
class PostActiveManager(PostMainManager):
    conditions_default = Q(is_active=True, is_deleted=False)

    def filter_readonly(self, user=None):
        conditions_public = Q(public_type='PUBLIC') & (
            (
                Q(is_reserved=False) |
                (Q(is_reserved=True) & Q(reserved_at__lte=now()))
            ) & (
                Q(is_boomed=False) |
                (Q(is_boomed=True) & Q(boomed_at__gte=now()))
            )
        )

        conditions_only_friend = Q(public_type='FRIEND')

        if user and user.id:
            conditions_only_me = Q(user=user) & (
                Q(public_type='ONLY_ME') |
                (Q(public_type='PUBLIC') & Q(is_reserved=True) & Q(boomed_at__gte=now()))
            )
            return super().get_queryset().filter(
                self.conditions_default &
                (conditions_public | conditions_only_friend | conditions_only_me)
            )

        else:
            return super().get_queryset().filter(
                self.conditions_default & conditions_public
            )

    def get_queryset(self):
        conditions_public = Q(public_type='PUBLIC') & (
            (
                Q(is_reserved=False) |
                (Q(is_reserved=True) & Q(reserved_at__lte=now()))
            ) & (
                Q(is_boomed=False) |
                (Q(is_boomed=True) & Q(boomed_at__gte=now()))
            )
        )

        return super().get_queryset().filter(
            self.conditions_default & conditions_public
        )
