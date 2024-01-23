# Django
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import Max

# Mixins
from community.apps.boards.models.mixins import BoardPostModelMixin, BoardCommentModelMixin, BoardPermissionMixin

# Local
from community.bases.models import Model

# Modules
from community.modules.choices import VIEW_MODE_CHOICES, BOARD_TYPE_CHOICES, BOARD_GROUP_TYPE_CHOICES


# Main Section
class BoardGroup(Model):
    community = models.ForeignKey('communities.Community', verbose_name=_('Club'), on_delete=models.CASCADE,
                                  related_name='board_groups')
    community_title = models.CharField(_('Community Title'), max_length=60, null=True, blank=True)
    title = models.CharField(_('Title'), max_length=100)
    order = models.IntegerField(_('Order'), default=1, validators=[MinValueValidator(1)])
    type = models.CharField(_('Type'), choices=BOARD_GROUP_TYPE_CHOICES, max_length=100, default='NORMAL')

    __is_active = None
    __title = None

    class Meta:
        verbose_name = verbose_name_plural = _('Board Group')
        ordering = ['order']

    def __str__(self):
        return f'{self.community_title} {self.title}'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__is_active = self.is_active
        self.__title = self.title

    def save(self, *args, **kwargs):
        if self.id is None:
            # Set BoardGroup Field
            if self.community:
                self.community_title = self.community.title

            # 커뮤니티에 엮인 보드 그룹의 order 최대 값 + 1
            max_board_group = self.community.board_groups.aggregate(order=Max('order'))
            if not max_board_group['order']:
                max_board_group['order'] = 0
            total_num = max_board_group['order'] + 1
            self.order = total_num

        else:
            # 보드 그룹을 비 활성화 상태로 변경 시, 하위 보드를 모두 비 활성화 상태로 변경
            if self.__is_active and not self.is_active:
                active_boards = self.boards.filter(is_active=True, is_deleted=False)
                if active_boards:
                    active_board_list = []
                    for active_board in active_boards:
                        active_board.is_active = False
                        active_board_list.append(active_board)
                    Board.objects.bulk_update(active_board_list, ['is_active'])

        return super(BoardGroup, self).save(*args, **kwargs)


class Board(BoardPostModelMixin,
            BoardCommentModelMixin,
            BoardPermissionMixin,
            Model):
    community = models.ForeignKey('communities.Community', verbose_name=_('Community'), on_delete=models.CASCADE,
                                  related_name='boards', null=True)
    community_title = models.CharField(_('Community Title'), max_length=60, null=True, blank=True)
    board_group = models.ForeignKey('BoardGroup', verbose_name=_('Board Group'), on_delete=models.SET_NULL, null=True,
                                    blank=True, related_name='boards')
    board_group_title = models.CharField(_('Board Group Title'), max_length=60, null=True, blank=True)
    title = models.CharField(_('Title'), max_length=20)
    description = models.CharField(_('Description'), max_length=160, null=True, blank=True)
    view_mode = models.CharField(_('View Mode'), choices=VIEW_MODE_CHOICES, max_length=100, default='LIST_TYPE')
    type = models.CharField(_('Type'), choices=BOARD_TYPE_CHOICES, max_length=100, default='NORMAL')
    order = models.IntegerField(_('Order'), default=1, validators=[MinValueValidator(1)])

    __title = None
    __read_permission = None

    class Meta:
        verbose_name = verbose_name_plural = _('Board')
        ordering = ['order']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__title = self.title
        self.__read_permission = self.read_permission

    def __str__(self):
        return f'{self.community_title}/{self.title}'

    def save(self, *args, **kwargs):
        if self.id is None:
            # 보드 그룹에 엮인 보드의 order 최대 값 + 1
            # max_board = self.board_group.boards.aggregate(order=Max('order'))
            # if not max_board['order']:
            #     max_board['order'] = 0
            # total_num = max_board['order'] + 1
            # self.order = total_num

            # Set Board Field
            self.community_title = self.community.title
            # self.board_group_title = self.board_group.title

        # else:
        #     if not self.board_group.is_active:
        #         raise ParseError('비 활성화 상태의 보드 그룹 에서 보드의 상태 변경은 불가능 합니다.')

        return super(Board, self).save(*args, **kwargs)
