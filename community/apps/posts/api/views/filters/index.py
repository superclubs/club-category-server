# Python
from datetime import timedelta

# Django
import django_filters
from django_filters import CharFilter, NumberFilter, BooleanFilter
from django.utils.timezone import now

# Models
from community.apps.posts.models import Post
from community.apps.comments.models import Comment
from community.apps.likes.models import PostLike
from community.apps.profiles.models import Profile


# Main Section
class PostFilter(django_filters.FilterSet):
    profile = NumberFilter(field_name='profile')
    tag_title = CharFilter(field_name='post_tags__tag__title')
    public_type = CharFilter(field_name='public_type')
    public_type__not = CharFilter(field_name='public_type', exclude=True)

    is_temporary = BooleanFilter(method='is_temporary_filter')
    is_notice = BooleanFilter(field_name='is_notice')

    is_subscribed = BooleanFilter(method='is_subscribed_filter')

    profile_liked = NumberFilter(method='profile_liked_filter')
    profile_commented = NumberFilter(method='profile_commented_filter')
    date = CharFilter(method='date_filter')

    class Meta:
        model = Post
        fields = ['date', 'profile', 'profile_liked', 'profile_commented', 'tag_title', 'public_type',
                  'public_type__not', 'is_notice', 'is_temporary']

    def date_filter(self, queryset, title, value):
        today = now()
        week_ago = today - timedelta(days=1)
        month_ago = today - timedelta(days=7)
        year_ago = today - timedelta(days=30)

        if value == 'week':
            return queryset.filter(created__range=[week_ago, today])
        elif value == 'month':
            return queryset.filter(created__range=[month_ago, today])
        elif value == 'year':
            return queryset.filter(created__range=[year_ago, today])

    def profile_liked_filter(self, queryset, title, value):
        profile = Profile.available.filter(id=value).first()
        if profile:
            post_ids = PostLike.available.filter(profile=profile, is_active=True, is_deleted=False).values_list('post_id', flat=True)
        return queryset.filter(id__in=post_ids)

    def profile_commented_filter(self, queryset, title, value):
        profile = Profile.available.filter(id=value).first()
        if profile:
            post_ids = Comment.available.filter(profile=profile, is_active=True, is_deleted=False).values_list('post_id', flat=True)
        return queryset.filter(id__in=post_ids)

    def is_temporary_filter(self, queryset, title, value):
        if value:
            user = self.request.user
            if user.id is None:
                queryset = queryset.none()
            else:
                queryset = queryset.filter(is_temporary=True, user=user)

        else:
            queryset = queryset.filter(is_temporary=value)

        return queryset


class CommunityPostFilter(django_filters.FilterSet):
    profile = NumberFilter(field_name='profile')
    tag_title = CharFilter(field_name='post_tags__tag__title')
    public_type = CharFilter(field_name='public_type')
    public_type__not = CharFilter(field_name='public_type', exclude=True)

    is_temporary = BooleanFilter(field_name='is_temporary')
    is_notice = BooleanFilter(field_name='is_notice')
    is_event = BooleanFilter(field_name='is_event')
    is_bookmarked = BooleanFilter(method='is_bookmarked_filter')

    class Meta:
        model = Post
        fields = ['profile', 'tag_title', 'public_type', 'public_type__not', 'is_notice', 'is_event', 'is_temporary',
                  'is_bookmarked']

    def is_bookmarked_filter(self, queryset, title, value):
        user = self.request.user
        if not user.id:
            return queryset

        if value:
            bookmarked_post_ids = user.post_bookmarks.filter(is_active=True, is_deleted=False).values_list('post', flat=True)
            queryset = queryset.filter(id__in=bookmarked_post_ids)

        return queryset


class BoardPostFilter(django_filters.FilterSet):
    public_type__not = CharFilter(field_name='public_type', exclude=True)
    is_temporary = BooleanFilter(field_name='is_temporary')

    is_notice = BooleanFilter(field_name='is_notice')
    is_event = BooleanFilter(field_name='is_event')
    date = CharFilter(method='date_filter')

    class Meta:
        model = Post
        fields = ['date', 'public_type__not', 'is_temporary', 'is_notice', 'is_event']

    def date_filter(self, queryset, title, value):
        today = now()
        week_ago = today - timedelta(days=1)
        month_ago = today - timedelta(days=7)
        year_ago = today - timedelta(days=30)

        if value == 'week':
            return queryset.filter(created__range=[week_ago, today])
        elif value == 'month':
            return queryset.filter(created__range=[month_ago, today])
        elif value == 'year':
            return queryset.filter(created__range=[year_ago, today])


class PostsAdminFilter(django_filters.FilterSet):
    board = NumberFilter(field_name='board')
    is_active = BooleanFilter(field_name='is_active')

    class Meta:
        model = Post
        fields = ['board', 'is_active']
