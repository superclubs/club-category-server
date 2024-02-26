# Django
from django.contrib import admin
from django.utils.html import format_html
from django.contrib import messages

# Bases
from community.bases.admin import Admin

# Models
from community.apps.comments.models import Comment


@admin.register(Comment)
class CommentAdmin(Admin):
    list_display = ('profile_image_tag', 'community', 'post', 'user',
                    'like_count', 'dislike_count', 'reported_count',
                    'is_secret', 'is_active')
    search_fields = ('post__title', 'user__username',)
    list_filter = ('is_secret',)
    ordering = ('-created',)

    fieldsets = (
        ('1. 정보', {'fields': ('community', 'post', 'parent_comment')}),
        ('2. 본문', {'fields': ('content',)}),
        ('3. 유저', {'fields': ('profile_image_tag', 'user')}),
        ('4. 통계', {'fields': ('like_count', 'dislike_count', 'reported_count')}),
        ('5. 비밀글 및 활성화 여부', {'fields': ('is_secret', 'is_active')}),
        ('6. 생성 및 수정 시간', {'fields': ('created', 'modified')})
    )

    readonly_fields = ('like_count', 'dislike_count', 'profile_image_tag', 'reported_count', 'created', 'modified')
    inline_actions = ['create_comment_like', 'create_comment_dislike']

    def profile_image_tag(self, obj):
        if obj.user.profile_image_url:
            return format_html('<img src="{}" width="100px;"/>'.format(obj.user.profile_image_url))

    profile_image_tag.short_description = '프로필'

    def create_comment_like(self, request, obj, parent_obj=None):
        obj.create_comment_like()
        messages.success(request, '댓글 좋아요가 생성됐습니다.')

    def create_comment_dislike(self, request, obj, parent_obj=None):
        obj.create_comment_dislike()
        messages.success(request, '댓글 싫어요가 생성됐습니다.')
