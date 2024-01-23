# Django
import django_filters
from django_filters import NumberFilter, BooleanFilter
from django.utils.timezone import now
from django.utils.functional import cached_property
from django.db.models import Q

# DRF
from rest_framework.exceptions import ParseError

# Models
from community.apps.post_tags.models import PostTag
from community.apps.tags.models import Tag


# Main Section
class TagFilter(django_filters.FilterSet):
    community = NumberFilter(method='community_filter')
    has_posts = BooleanFilter(method='has_posts_filter')
    has_bookmark_posts = BooleanFilter(method='has_bookmark_posts_filter')

    class Meta:
        model = Tag
        fields = ['community', 'has_posts', 'has_bookmark_posts']

    @cached_property
    def invisible_post_tags(self):
        return PostTag.available.filter(Q(post__public_type='ONLY_ME') |
                                      Q(post__is_temporary=True) |
                                      Q(post__is_reserved=True, post__reserved_at__lte=now()))

    def community_filter(self, queryset, title, value):
        tag_ids = PostTag.available.filter(post__community=value).values_list('tag_id', flat=True)
        return queryset.filter(id__in=tag_ids)

    # TODO: 예약 게시글이 보여지는 순간 tag.post_count 증가 로직 필요
    def has_posts_filter(self, queryset, title, value):
        if value:
            queryset = queryset.filter(post_count__gt=0)

            invisible_post_tags = self.invisible_post_tags
            if invisible_post_tags:
                tag_ids = invisible_post_tags.values_list('tag__id', flat=True)
                return queryset.exclude(id__in=tag_ids)

        return queryset

    def has_subscribe_posts_filter(self, queryset, title, value):
        if value:
            user = self.request.user
            if not user.id:
                raise ParseError('anonymous user')

            subscribe_posts = user.subscribe_posts.filter(is_active=True, is_deleted=False)
            subscribe_posts_ids = subscribe_posts.values_list('post__id', flat=True)

            subscribe_post_tags = PostTag.available.filter(post__in=subscribe_posts_ids)

            # Exclude Invisible Post Tag
            invisible_post_tags = self.invisible_post_tags
            if invisible_post_tags:
                invisible_post_tags_ids = invisible_post_tags.values_list('tag__id', flat=True)
                subscribe_post_tags = subscribe_post_tags.exclude(tag__id__in=invisible_post_tags_ids)

            tag_ids = subscribe_post_tags.values_list('tag__id', flat=True)

            return queryset.filter(id__in=tag_ids)

        return queryset

    def has_bookmark_posts_filter(self, queryset, title, value):
        if value:
            user = self.request.user
            if not user.id:
                raise ParseError('anonymous user')

            bookmark_post_ids = user.post_bookmarks.filter(is_active=True, is_deleted=False).values_list('post', flat=True)
            bookmark_post_tags = PostTag.available.filter(post__in=bookmark_post_ids)

            # Exclude Invisible Post Tag
            invisible_post_tags = self.invisible_post_tags
            if invisible_post_tags:
                invisible_post_tags_ids = invisible_post_tags.values_list('tag__id', flat=True)
                bookmark_post_tags = bookmark_post_tags.exclude(tag__id__in=invisible_post_tags_ids)

            tag_ids = bookmark_post_tags.values_list('tag__id', flat=True)

            return queryset.filter(id__in=tag_ids)

        return queryset
