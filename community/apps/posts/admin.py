# Django
from django.contrib import admin
from django.utils.html import format_html

# Models
from community.apps.posts.models.index import Post
# Bases
from community.bases.admin import Admin


# Function Section
def delete_selected_softly(modeladmin, request, queryset):
    posts = queryset.all()
    for post in posts:
        post.soft_delete()


class PostAdmin(Admin):
    list_display = (
        "thumbnail_media_tag",
        "user",
        "title",
        "community",
        "visit_count",
        "comment_count",
        "like_count",
        "is_active",
        "web_url",
    )
    search_fields = ("user__username", "title", "community__title")
    list_filter = ("community",)

    fieldsets = (
        ("1. 정보", {"fields": ("community", "board", "title", "content", "web_url")}),
        ("2. 이미지", {"fields": ("thumbnail_media_tag", "thumbnail_media_url")}),
        ("3. 유저", {"fields": ("user", "profile")}),
        (
            "4. 통계",
            {
                "fields": (
                    "point",
                    "like_count",
                    "dislike_count",
                    "comment_count",
                    "bookmark_count",
                    "visit_count",
                    "reported_count",
                    "share_count",
                )
            },
        ),
        ("5. 활성화 유무", {"fields": ("is_active",)}),
        ("6. 생성일", {"fields": ("created", "achieved_20_points_at")}),
    )

    readonly_fields = (
        "achieved_20_points_at",
        "thumbnail_media_tag",
        "thumbnail_media_url",
        "like_count",
        "dislike_count",
        "comment_count",
        "bookmark_count",
        "visit_count",
        "reported_count",
        "share_count",
        "web_url",
    )
    summernote_fields = ("content",)

    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields

    def thumbnail_media_tag(self, obj):
        if obj.thumbnail_media_url:
            return format_html('<img src="{}" width="100px;"/>'.format(obj.thumbnail_media_url))

    thumbnail_media_tag.short_description = "썸네일"

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        super(PostAdmin, self).save_model(request, obj, form, change)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            actions["delete_selected"] = (delete_selected_softly, "delete_selected", "소프트 삭제")
        return actions
