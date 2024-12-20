from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from community.apps.emojis.models import CommentEmoji


# Main Section
@receiver(pre_save, sender=CommentEmoji)
def comment_emoji_pre_save(sender, instance, *args, **kwargs):
    print("========== CommentEmoji pre_save ==========")

    if not instance.id:
        instance._is_changed = False
    else:
        _instance = CommentEmoji.objects.filter(id=instance.id).first()
        instance._is_changed = _instance.emoji_code != instance.emoji_code


@receiver(post_save, sender=CommentEmoji)
def count_comment_emoji_post_save(sender, instance, created, **kwargs):
    print("========== CommentEmoji post_save : Count ==========")

    comment = instance.comment
    post = comment.post
    is_changed = instance._is_changed

    if created or is_changed:
        comment.update_emoji_count()

        # Post PostEmoji Count
        post.update_comments_emoji_count()

        # Profile PostEmoji Count
        instance.profile.update_profile_comments_emoji_count()


@receiver(post_delete, sender=CommentEmoji)
def post_emoji_post_delete(sender, instance, *args, **kwargs):
    print("========== CommentEmoji post_delete ==========")
    # 1. 카운트 감소
    # 2. friend point history 추가

    comment = instance.comment
    post = comment.post

    # Comment emoji Count
    comment.update_emoji_count()

    # Post CommentEmoji Count
    post.update_comments_emoji_count()

    # Profile CommentEmoji Count
    instance.profile.update_profile_comments_emoji_count()
