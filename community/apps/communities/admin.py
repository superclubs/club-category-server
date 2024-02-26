# Django
from django.contrib import admin
from django.utils.safestring import mark_safe

# Bases
from community.bases.admin import Admin

# Models
from community.apps.communities.models import Community


@admin.register(Community)
class CommunityAdmin(Admin):
    list_display = ('title', 'address_reference', 'user', 'level')

    search_fields = ('user__username', 'address', 'title')
    list_filter = ('level',)
    ordering = ()

    fieldsets = (
        ('1. 정보', {'fields': ('id', 'parent_community', 'title', 'user', 'description', 'address', 'level', 'point')}),
        ('2. 이미지', {'fields': ('banner_image', 'banner_image_url')}),
        ('3. 전체 통계', {'fields': ('post_count', 'comment_count')}),
        ('4. 활성화 유무', {'fields': ('is_active',)}),
        ('5. 생성일 / 수정일', {'fields': ('created', 'modified')}),
    )

    readonly_fields = ('id', 'created', 'modified', 'user_data', 'point', 'title', 'address', 'banner_image_url',
                       'post_count', 'comment_count')

    def address_reference(self, obj):
        return mark_safe(
            f'<a style="display: inline-block; width: 120px; word-wrap:break-word !important;" href="{obj.address}" target="_blank">{obj.address}</a>')

    address_reference.short_description = '웹'
