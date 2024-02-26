# Django
from django.contrib import admin

# Models
from community.apps.profiles.models import Profile

# Bases
from community.bases.admin import Admin


@admin.register(Profile)
class ProfileAdmin(Admin):
    list_display = ('community', 'user', 'level', 'point', 'community_visit_count', 'post_count', 'comment_count',
                    'is_active')
    fieldsets = (
        ('1. 정보', {'fields': ('community', 'user',)}),
        ('2. 카운트', {'fields': ('post_count', 'comment_count', 'community_visit_count')}),
        ('3. 유저 정보', {'fields': ('point', 'level')})
    )

    readonly_fields = ('post_count', 'comment_count', 'community_visit_count', 'point')
