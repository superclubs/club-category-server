# Django
from django.utils.html import format_html
from django.contrib import messages

# Models
from community.apps.posts.models.index import Post

# Bases
from community.bases.admin import Admin
from django.contrib import admin


@admin.register(Post)
class PostAdmin(Admin):
    list_display = ('thumbnail_media_tag', 'user', 'title', 'community',
                    'visit_count', 'comment_count', 'like_count',
                    'is_active', 'web_url')
    search_fields = ('user__username', 'title', 'community__title')
    list_filter = ('community',)

    fieldsets = (
        ('1. 정보', {'fields': ('community', 'board', 'title', 'content', 'web_url')}),
        ('2. 이미지', {'fields': ('thumbnail_media_tag', 'thumbnail_media_url')}),
        ('3. 유저', {'fields': ('user', 'profile')}),
        ('4. 통계', {'fields': ('point', 'like_count', 'dislike_count', 'comment_count', 'bookmark_count', 'visit_count',
                              'reported_count', 'share_count')}),
        ('5. 활성화 유무', {'fields': ('is_active',)}),
        ('6. 생성일', {'fields': ('created', 'achieved_20_points_at')}),
    )

    readonly_fields = ('achieved_20_points_at', 'thumbnail_media_tag', 'thumbnail_media_url',
                       'like_count', 'dislike_count', 'comment_count', 'bookmark_count', 'visit_count', 'reported_count',
                       'share_count', 'web_url')
    summernote_fields = ('content',)
    # inline_actions = ['create_post_like', 'create_post_dislike']

    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields

    def thumbnail_media_tag(self, obj):
        if obj.thumbnail_media_url:
            return format_html('<img src="{}" width="100px;"/>'.format(obj.thumbnail_media_url))

    thumbnail_media_tag.short_description = '썸네일'

    # 어드민 사이트에서 유저 필드 넣는 함수
    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        super(PostAdmin, self).save_model(request, obj, form, change)

    # def create_post_like(self, request, obj, parent_obj=None):
    #     obj.create_post_like()
    #     messages.success(request, '포스트 좋아요가 생성됐습니다.')
    #
    # def create_post_dislike(self, request, obj, parent_obj=None):
    #     obj.create_post_dislike()
    #     messages.success(request, '포스트 싫어요가 생성됐습니다.')
