from django.contrib import admin

from community.apps.boards.models import Board, BoardGroup
from community.bases.admin import Admin
from community.bases.inlines import StackedInline


class BoardInline(StackedInline):
    model = Board
    fieldsets = (
        ('보드', {'fields': ('title',)}),
    )
    extra = 0


@admin.register(BoardGroup)
class BoardGroupAdmin(Admin):
    list_display = ('community', 'title')
    search_fields = ('community__title',)
    list_filter = ('community',)

    fieldsets = (
        ('1. 정보', {'fields': ('community', 'title')}),
        ('2. 활성화 여부', {'fields': ('is_active',)}),
    )
    add_fieldsets = (
        ('1. 정보', {'fields': ('community', 'title')}),
        ('2. 활성화 여부', {'fields': ('is_active',)}),
    )

    inlines = (BoardInline,)


@admin.register(Board)
class BoardAdmin(Admin):
    list_display = ('community', 'board_group', 'title', 'is_active')
    search_fields = ('board_group__title',)
    list_filter = ('board_group',)

    fieldsets = (
        ('1. 정보', {'fields': ('community', 'board_group', 'title',)}),
        ('2. 활성화 여부', {'fields': ('is_active',)}),
        ('3. 보드 권한',
         {'fields': ('write_permission', 'read_permission')}),
    )
    add_fieldsets = (
        ('1. 정보', {'fields': ('community', 'board_group', 'title',)}),
        ('2. 활성화 여부', {'fields': ('is_active',)}),
        ('3. 보드 권한',
         {'fields': ('write_permission', 'read_permission')})
    )
    readonly_fields = ()


