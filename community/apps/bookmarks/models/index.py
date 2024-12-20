from django.db import models
from django.utils.translation import gettext_lazy as _

from community.bases.models import Model
from community.modules.producers.bookmark import BookmarkProducer


# Main Section
class PostBookmark(Model):
    post = models.ForeignKey(
        "posts.Post", verbose_name=_("Post"), on_delete=models.CASCADE, related_name="post_bookmarks"
    )
    user = models.ForeignKey(
        "users.User", verbose_name=_("User"), on_delete=models.SET_NULL, null=True, related_name="post_bookmarks"
    )
    __is_active = None

    class Meta:
        verbose_name = verbose_name_plural = _("Post Bookmark")
        ordering = ["-created"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__is_active = self.is_active

    def save(self, *args, **kwargs):
        is_created = self._state.adding
        if is_created:
            # User PostBookmark Count
            self.user.increase_user_post_bookmark_count()
            self.user.save()

            # PostBookmark Count
            self.post.increase_post_bookmark_count()
            self.post.save()

        else:
            if self.__is_active != self.is_active:
                # Update User, Post PostBookmark Count
                if self.is_active:
                    self.user.increase_user_post_bookmark_count()
                    self.post.increase_post_bookmark_count()

                else:
                    self.user.decrease_user_post_bookmark_count()
                    self.post.decrease_post_bookmark_count()

                self.user.save()
                self.post.save()

        super(PostBookmark, self).save(*args, **kwargs)

        if is_created:
            BookmarkProducer().create_bookmark(self)
        else:
            if self.__is_active != self.is_active:
                BookmarkProducer().create_bookmark(self) if self.is_active else BookmarkProducer().delete_bookmark(self)
