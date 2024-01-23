# Manager
from community.apps.comments.models.managers.objects import CommentMainManager


# Main Section
class CommentActiveManager(CommentMainManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True, is_deleted=False, parent_comment=None)
