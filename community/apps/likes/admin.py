# Django
from django.contrib import admin

# Bases
from community.bases.admin import Admin

# Models
from community.apps.likes.models import CommentLike, CommentDislike, PostLike, PostDislike


# Main Section
@admin.register(CommentLike)
class CommentLikeAdmin(Admin):
    list_display = ('comment', 'user')
    search_fields = ('comment__post', 'user__email')

    fieldsets = (
        ('정보', {'fields': ('comment', 'user')}),
    )


@admin.register(CommentDislike)
class CommentDislikeAdmin(Admin):
    list_display = ('comment', 'user')
    search_fields = ('comment__post', 'user__email')

    fieldsets = (
        ('정보', {'fields': ('comment', 'user')}),
    )


@admin.register(PostLike)
class PostLikeAdmin(Admin):
    list_display = ('post', 'user')
    search_fields = ('post__title', 'user__email')

    fieldsets = (
        ('정보', {'fields': ('post', 'user')}),
    )


@admin.register(PostDislike)
class PostDislikeAdmin(Admin):
    list_display = ('post', 'user')
    search_fields = ('post__title', 'user__email')

    fieldsets = (
        ('정보', {'fields': ('post', 'user')}),
    )
