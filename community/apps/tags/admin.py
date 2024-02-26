from django.contrib import admin

from community.apps.tags.models.index import Tag
from community.bases.admin import CountAdmin


@admin.register(Tag)
class TagAdmin(CountAdmin):
    list_display = ('title', 'community_count', 'post_count')
    ordering = ('community_count', 'post_count')

    fieldsets = (
        ('1. 정보', {'fields': ('title',)}),
        ('2. 카운트', {'fields': ('community_count', 'post_count')})
    )

    readonly_fields = ('title', 'community_count', 'post_count')
