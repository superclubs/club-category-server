# Django
from django.contrib import admin
from django.utils.html import format_html

# Bases
from community.bases.admin import Admin

# Models
from community.apps.badges.models import Badge


# Main Section
@admin.register(Badge)
class BadgeAdmin(Admin):
    list_display = ('image_tag', 'title', 'model_type')
    search_fields = ('title', 'model_type')
    list_filter = ('model_type',)
    ordering = ()

    fieldsets = (
        ('1. 정보', {'fields': ('title', 'model_type')}),
        ('2. 이미지', {'fields': ('image_tag', 'image', 'image_url')}),
        ('3. 활성화 유무', {'fields': ('is_active',)}),
        ('4. 생성일 / 수정일', {'fields': ('created', 'modified')}),
    )

    readonly_fields = ('created', 'modified', 'image_tag', 'image_url')

    def image_tag(self, obj):
        if obj.image_url:
            return format_html('<img src="{}" width="100px;"/>'.format(obj.image_url))
        if obj.image:
            return format_html('<img src="{}" width="100px;"/>'.format(obj.image.url))

    image_tag.short_description = '이미지'
