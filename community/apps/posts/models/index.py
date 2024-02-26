# Python
from datetime import timedelta

# Django
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.db.models import Q

# Models
from community.apps.badges.models import Badge

# Managers
from community.apps.posts.models.managers.active import PostActiveManager

# Bases
from community.bases.models import Model

# Mixins
from community.apps.posts.models.mixins import PostCommentModelMixin, PostLikeModelMixin, PostShareModelMixin, \
    PostVisitModelMixin, PostTagModelMixin, PostReportModelMixin, PostRankModelMixin, PostBadgeModelMixin, \
    PostMediaModelMixin, PostBookmarkModelMixin, PostPointModelMixin

# Bases
from community.bases.models import Manager

# Modules
from community.modules.choices import PUBLIC_TYPE_CHOICES, BOOM_PERIOD_CHOICES

# Utils
from community.utils.fields import extract_content_summary



# Manager Section
class PostBadgeManager(Manager):
    def get_new_badge(self):
        # 1. Get New Badge
        new_badge = Badge.available.get(title='New', model_type='POST')

        # 2. Get Posts
        date = now() - timedelta(days=7)
        q_created = Q(created__gte=date)
        q_badge = Q(badges=new_badge)
        new_posts = Post.available.filter(q_created & ~q_badge)
        old_posts = Post.available.filter(~q_created & q_badge)

        # 3. Update
        for post in new_posts:
            post.badges.add(new_badge.id)

        for post in old_posts:
            post.badges.remove(new_badge)

    def get_grade_badge(self):

        nice_badge = Badge.available.get(title='Nice', model_type='POST')
        good_badge = Badge.available.get(title='Good', model_type='POST')
        excellent_badge = Badge.available.get(title='Excellent', model_type='POST')
        great_badge = Badge.available.get(title='Great', model_type='POST')
        wonderful_badge = Badge.available.get(title='Wonderful', model_type='POST')
        fantastic_badge = Badge.available.get(title='Fantastic', model_type='POST')
        amazing_badge = Badge.available.get(title='Amazing', model_type='POST')

        nice_posts = Post.available.filter(Q(point__range=[100, 499]), ~Q(badges=nice_badge))
        good_posts = Post.available.filter(Q(point__range=[500, 999]), ~Q(badges=good_badge))
        excellent_posts = Post.available.filter(Q(point__range=[1000, 2999]), ~Q(badges=excellent_badge))
        great_posts = Post.available.filter(Q(point__range=[3000, 4999]), ~Q(badges=great_badge))
        wonderful_posts = Post.available.filter(Q(point__range=[5000, 9999]), ~Q(badges=wonderful_badge))
        fantastic_posts = Post.available.filter(Q(point__range=[10000, 14999]), ~Q(badges=fantastic_badge))
        amazing_posts = Post.available.filter(Q(point__gte=15000), ~Q(badges=amazing_badge))

        for post in nice_posts:
            post.badges.add(nice_badge.id)

        for post in good_posts:
            post.badges.remove(nice_badge)
            post.badges.add(good_badge.id)

        for post in excellent_posts:
            post.badges.remove(good_badge, nice_badge)
            post.badges.add(excellent_badge.id)

        for post in great_posts:
            post.badges.remove(excellent_badge, good_badge, nice_badge)
            post.badges.add(great_badge.id)

        for post in wonderful_posts:
            post.badges.remove(great_badge, excellent_badge, good_badge, nice_badge)
            post.badges.add(wonderful_badge.id)

        for post in fantastic_posts:
            post.badges.remove(wonderful_badge, great_badge, excellent_badge, good_badge, nice_badge)
            post.badges.add(fantastic_badge.id)

        for post in amazing_posts:
            post.badges.remove(fantastic_badge, wonderful_badge, great_badge, excellent_badge, good_badge, nice_badge)
            post.badges.add(amazing_badge.id)


# Main Section
class Post(PostCommentModelMixin,
           PostLikeModelMixin,
           PostShareModelMixin,
           PostVisitModelMixin,
           PostBookmarkModelMixin,
           PostTagModelMixin,
           PostReportModelMixin,
           PostRankModelMixin,
           PostBadgeModelMixin,
           PostMediaModelMixin,
           PostPointModelMixin,
           Model):
    # Club
    community = models.ForeignKey('communities.Community', verbose_name=_('Community'), on_delete=models.CASCADE,
                                  related_name='posts')
    community_title = models.CharField(_('Community Title'), max_length=60, null=True, blank=True)

    # Board Group
    board_group = models.ForeignKey('boards.BoardGroup', verbose_name=_('Board Group'), on_delete=models.SET_NULL,
                                    null=True, related_name='posts')
    board_group_title = models.CharField(_('Board Group Title'), max_length=60, null=True, blank=True)

    # Board
    board = models.ForeignKey('boards.Board', verbose_name=_('Board'), on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='posts')
    board_title = models.CharField(_('Board Title'), max_length=60, null=True, blank=True)
    read_permission = models.IntegerField(_('Read Permission'), null=True, blank=True)

    # FK
    badges = models.ManyToManyField('badges.Badge', verbose_name=_('Badge'), related_name='posts', blank=True)
    user = models.ForeignKey('users.User', verbose_name=_('User'), on_delete=models.SET_NULL, null=True, blank=True,
                             related_name='posts')
    user_data = models.JSONField(_('User Data'), null=True, blank=True)
    profile = models.ForeignKey('profiles.Profile', verbose_name=_('Profile'), on_delete=models.SET_NULL, null=True,
                                blank=True, related_name='posts')
    profile_data = models.JSONField(_('Profile Data'), null=True, blank=True)

    # Main
    title = models.CharField(_('Title'), max_length=100, null=True, blank=True, default='Untitled')
    content = models.TextField(_('Content'), null=True, blank=True)
    content_summary = models.TextField(_('Content Summary'), null=True, blank=True)
    public_type = models.CharField(_('Public Type'), choices=PUBLIC_TYPE_CHOICES, max_length=100, default='PUBLIC')
    password = models.IntegerField(_('Password'), null=True, blank=True)
    reserved_at = models.DateTimeField(_('Reserved At'), null=True, blank=True)
    boomed_period = models.CharField(_('Boomed Period'), choices=BOOM_PERIOD_CHOICES, max_length=100, null=True,
                                     blank=True)
    boomed_at = models.DateTimeField(_('Boomed At'), null=True, blank=True)
    web_url = models.URLField(_('Web URL'), null=True, blank=True)

    # Boolean
    is_temporary = models.BooleanField(_('Is Temporary'), default=False)
    is_secret = models.BooleanField(_('Is Secret'), default=False)
    is_reserved = models.BooleanField(_('Is Reserved'), default=False)
    is_boomed = models.BooleanField(_('Is Boomed'), default=False)
    is_agenda = models.BooleanField(_('Is Agenda'), default=False)
    is_vote = models.BooleanField(_('Is Vote'), default=False)

    is_notice = models.BooleanField(_('Is Notice'), default=False)
    is_event = models.BooleanField(_('Is Event'), default=False)

    is_comment = models.BooleanField(_('Is Comment'), default=True)
    is_share = models.BooleanField(_('Is Share'), default=True)
    is_search = models.BooleanField(_('Is Search'), default=True)

    is_default = models.BooleanField(_('Is Default'), default=False)

    # Date
    created = models.DateTimeField(default=now)
    achieved_20_points_at = models.DateTimeField(_('Achieved 20 Points At'), null=True, blank=True)

    __public_type = None
    __is_temporary = None

    objects = PostBadgeManager()
    active = PostActiveManager()

    class Meta:
        verbose_name = verbose_name_plural = _('Post')
        ordering = ['-created']

    def __str__(self):
        return f'{self.id} / {self.title}'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__public_type = self.public_type
        self.__is_temporary = self.is_temporary

    def save(self, *args, **kwargs):
        if self.id is None:
            self.community_title = self.community.title

            if self.content:
                self.content_summary = extract_content_summary(self.content)

            if self.board:
                self.board_title = self.board.title
                self.read_permission = self.board.read_permission
                self.board_group = self.board.board_group
                self.board_group_title = self.board.board_group.title

            if not self.is_temporary and not self.is_agenda and not self.is_reserved and self.public_type != 'ONLY_ME':
                self.increase_related_model_post_count()

        else:
            if (self.__public_type == 'ONLY_ME' and self.__public_type != self.public_type) or (
                self.__is_temporary and not self.is_temporary):
                self.increase_related_model_post_count(post_tag=True)

            elif self.public_type == 'ONLY_ME' and self.__public_type != self.public_type:
                self.decrease_related_model_post_count(post_tag=True)

        # Point
        if self.point >= 20 and not self.achieved_20_points_at:
            self.achieved_20_points_at = now()

        return super(Post, self).save(*args, **kwargs)

    def increase_related_model_post_count(self, post_tag=False):
        # User Post Count
        self.user.increase_user_post_count()
        self.user.save()

        # Community Post Count
        self.community.increase_community_post_count()
        self.community.save()

        # Profile Post Count
        if self.profile:
            self.profile.increase_profile_post_count()
            self.profile.save()

        # Post Tag Post Count
        if post_tag:
            post_tags = self.post_tags.filter(is_active=True, is_deleted=False)
            for post_tag in post_tags:
                post_tag.tag.increase_tag_post_count()
                post_tag.tag.save()

    def decrease_related_model_post_count(self, post_tag=False):
        # User Post Count
        self.user.decrease_user_post_count()
        self.user.save()

        # Club Post Count
        self.community.decrease_community_post_count()
        self.community.save()

        # Profile Post Count
        self.profile.decrease_profile_post_count()
        self.profile.save()

        # Post Tag Post Count
        if post_tag:
            post_tags = self.post_tags.filter(is_active=True, is_deleted=False)
            for post_tag in post_tags:
                post_tag.tag.decrease_tag_post_count()
                post_tag.tag.save()
