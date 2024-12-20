# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

from community.apps.likes.constants.index import emoji_dict
# Models
from community.bases.models import Model

# Module
from community.modules.choices import LIKE_TYPE_CHOICES


# Main Section
class PostLike(Model):
    post = models.ForeignKey("posts.Post", verbose_name=_("Post"), on_delete=models.CASCADE, related_name="post_likes")
    user = models.ForeignKey("users.User", verbose_name=_("User"), on_delete=models.CASCADE, related_name="post_likes")
    profile = models.ForeignKey(
        "profiles.Profile", verbose_name=_("Profile"), on_delete=models.CASCADE, related_name="post_likes"
    )
    community = models.ForeignKey(
        "communities.Community", verbose_name=_("Community"), on_delete=models.CASCADE, related_name="post_likes"
    )
    profile_data = models.JSONField(_("Profile Data"), null=True, blank=True)
    user_data = models.JSONField(_("User Data"), null=True, blank=True)
    type = models.CharField(_("Type"), choices=LIKE_TYPE_CHOICES, max_length=100, null=True, blank=True)

    __type = None
    __is_active = None

    class Meta:
        verbose_name = verbose_name_plural = _("Post Like")
        ordering = ["-created"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__type = self.type
        self.__is_active = self.is_active

    def save(self, *args, **kwargs):
        # Variable Assignment
        post = self.post
        profile = self.profile
        community = post.community

        if self.id is None:
            # Profile PostLike Count
            profile.increase_profile_posts_like_count()
            profile.save()

            # Community PostLike Count
            community.increase_community_posts_like_count()
            community.save()

        else:
            # Unlike Section
            if self.__is_active != self.is_active:

                # Update Post, Profile, Club PostLike Count
                if self.is_active:
                    profile.increase_profile_posts_like_count()
                    community.increase_community_posts_like_count()

                else:
                    profile.decrease_profile_posts_like_count()
                    community.decrease_community_posts_like_count()

                community.save()
                profile.save()

        return super(PostLike, self).save(*args, **kwargs)


class PostDislike(Model):
    post = models.ForeignKey(
        "posts.Post", verbose_name=_("Post"), on_delete=models.CASCADE, related_name="post_dislikes"
    )
    user = models.ForeignKey(
        "users.User", verbose_name=_("User"), on_delete=models.CASCADE, related_name="post_dislikes"
    )
    profile = models.ForeignKey(
        "profiles.Profile", verbose_name=_("Profile"), on_delete=models.CASCADE, related_name="post_dislikes"
    )
    community = models.ForeignKey(
        "communities.Community", verbose_name=_("Community"), on_delete=models.CASCADE, related_name="post_dislikes"
    )
    __is_active = None

    class Meta:
        verbose_name = verbose_name_plural = _("Post Dislike")
        ordering = ["-created"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__is_active = self.is_active

    def save(self, *args, **kwargs):
        # Common Variable Assignment
        profile = self.profile
        community = self.community

        if self.id is None:
            # Profile PostDislike Count
            profile.increase_profile_posts_dislike_count()
            profile.save()

            # Community PostDislike Count
            community.increase_community_posts_dislike_count()
            community.save()

        else:
            # Undislike Section
            if self.__is_active != self.is_active:
                # Update Post, Profile, Club PostDisLike Count
                if self.is_active:
                    profile.increase_profile_posts_dislike_count()
                    community.increase_community_posts_dislike_count()

                else:
                    profile.decrease_profile_posts_dislike_count()
                    community.decrease_community_posts_dislike_count()

                community.save()
                profile.save()

        return super(PostDislike, self).save(*args, **kwargs)


class CommentLike(Model):
    comment = models.ForeignKey(
        "comments.Comment", verbose_name=_("Comment"), on_delete=models.CASCADE, related_name="comment_likes"
    )
    user = models.ForeignKey(
        "users.User", verbose_name=_("User"), on_delete=models.CASCADE, related_name="comment_likes"
    )
    profile = models.ForeignKey(
        "profiles.Profile", verbose_name=_("Profile"), on_delete=models.CASCADE, related_name="comment_likes"
    )
    type = models.CharField(_("Type"), choices=LIKE_TYPE_CHOICES, max_length=100, default="LIKE")
    __type = None
    __is_active = None

    class Meta:
        verbose_name = verbose_name_plural = _("Comment Like")
        ordering = ["-created"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__type = self.type
        self.__is_active = self.is_active

    def save(self, *args, **kwargs):
        # Common Variable Assignment
        comment = self.comment
        post = comment.post
        community = comment.community
        profile = self.profile

        create_emoji = (
            True
            if (
                self._state.adding
                or self.__type != self.type
                or (self.__is_active != self.is_active and self.is_active)
            )
            else False
        )

        delete_emoji = True if (self.__is_active != self.is_active and not self.is_active) else False

        if self._state.adding:
            # Comment CommentLike Count, Point
            comment.increase_comment_total_like_count()
            comment.increase_comment_point()
            increase_count = getattr(comment, f"increase_comment_{self.type.lower()}_count")
            increase_count()
            comment.save()

            # Profile CommentLike Count
            profile.increase_profile_comments_like_count()
            profile.save()

            # Post CommentLike Count
            post.increase_post_comments_like_count()
            post.save()

            # Community CommentLike Count
            community.increase_community_comments_like_count()
            community.save()

        else:
            # Unlike Section
            if self.__is_active != self.is_active:

                # Update Comment, Profile, Community CommentLike Count
                if self.is_active:
                    comment.increase_comment_total_like_count()
                    comment.increase_comment_point()

                    comment_count = getattr(comment, f"increase_comment_{self.type.lower()}_count")
                    comment_count()

                    profile.increase_profile_comments_like_count()
                    post.increase_post_comments_like_count()
                    community.increase_community_comments_like_count()

                else:
                    comment.decrease_comment_total_like_count()
                    comment.decrease_comment_point()

                    comment_count = getattr(comment, f"decrease_comment_{self.type.lower()}_count")
                    comment_count()

                    profile.decrease_profile_comments_like_count()
                    post.decrease_post_comments_like_count()
                    community.decrease_community_comments_like_count()

                comment.save()
                profile.save()
                post.save()
                community.save()

            # Change Like Section
            if self.__is_active == self.is_active and self.__type != self.type:
                # Update Comment CommentLike Count
                increase_count = getattr(comment, f"increase_comment_{self.type.lower()}_count")
                increase_count()
                decrease_count = getattr(comment, f"decrease_comment_{self.__type.lower()}_count")
                decrease_count()

                comment.save()

        super(CommentLike, self).save(*args, **kwargs)

        emoji_code = emoji_dict.get(self.type)

        if not emoji_code:
            return

        if create_emoji:
            # 좋아요 시 emoji 생성
            try:
                comment.emoji_comment(self.user, emoji_code)
            except Exception as e:
                print(f"Commentlike 생성 {e}")

        elif delete_emoji:
            # 좋아요 취소 시 emoji 삭제
            try:
                comment.unemoji_comment(self.user, emoji_code)
            except Exception as e:
                print(f"Commentlike 삭제 {e}")


class CommentDislike(Model):
    comment = models.ForeignKey(
        "comments.Comment", verbose_name=_("Comment"), on_delete=models.CASCADE, related_name="comment_dislikes"
    )
    user = models.ForeignKey(
        "users.User", verbose_name=_("User"), on_delete=models.CASCADE, related_name="comment_dislikes"
    )
    profile = models.ForeignKey(
        "profiles.Profile", verbose_name=_("Profile"), on_delete=models.CASCADE, related_name="comment_dislikes"
    )
    __is_active = None

    class Meta:
        verbose_name = verbose_name_plural = _("Comment Dislike")
        ordering = ["-created"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__is_active = self.is_active

    def save(self, *args, **kwargs):
        # Common Variable Assignment
        comment = self.comment
        profile = self.profile
        post = comment.post
        community = post.community

        if self.id is None:
            # Comment CommentDislike Count
            comment.increase_comment_dislike_count()
            comment.increase_comment_point()
            comment.save()

            # Profile CommentDislike Count
            profile.increase_profile_comments_dislike_count()
            profile.save()

            # Post CommentDislike Count
            post.increase_post_comments_dislike_count()
            post.save()

            # Community CommentDislike Count
            community.increase_community_comments_dislike_count()
            community.save()

        else:
            # Undislike Section
            if self.__is_active != self.is_active:
                # Update Comment, Profile, Community CommentDisLike Count
                if self.is_active:
                    comment.increase_comment_dislike_count()
                    comment.increase_comment_point()
                    profile.increase_profile_comments_dislike_count()
                    post.increase_post_comments_dislike_count()
                    community.increase_community_comments_dislike_count()
                else:
                    comment.decrease_comment_dislike_count()
                    comment.decrease_comment_point()
                    profile.decrease_profile_comments_dislike_count()
                    post.decrease_post_comments_dislike_count()
                    community.decrease_community_comments_dislike_count()

                comment.save()
                profile.save()
                post.save()
                community.save()

        return super(CommentDislike, self).save(*args, **kwargs)
