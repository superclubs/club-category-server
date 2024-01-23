# Django
from django.db import models
from django.utils.translation import gettext_lazy as _


# Main Section
class UserFriendModelMixin(models.Model):
    friend_count = models.IntegerField(_('Friend Count'), default=0)

    class Meta:
        abstract = True

    def check_friend(self, user):
        friend = self.my_friends.filter(user=user, is_active=True, is_deleted=False).first()
        if friend:
            return True
        return False
