# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Local
from django.utils.html import format_html

from community.bases.admin import Admin


class UserAdmin(Admin, UserAdmin):
    list_display = ("profile_image_tag", "username", "email", "is_staff", "web_url")
    search_fields = ("email", "username")
    list_filter = ()
    ordering = ("-created",)

    def profile_image_tag(self, obj):
        if obj.profile_image_url:
            return format_html('<img src="{}" width="100px;"/>'.format(obj.profile_image_url))

    profile_image_tag.short_description = "프로필"

    fieldsets = (
        ("1. 정보", {"fields": ("id", "email", "username", "password", "web_url")}),
        ("2. 이미지", {"fields": ("profile_image_tag", "profile_image_url")}),
        ("3. 권한", {"fields": ("is_staff",)}),
        ("4. 생성일 / 수정일", {"fields": ("created", "modified")}),
    )

    readonly_fields = ("created", "modified", "profile_image_tag", "profile_image_url", "web_url")
