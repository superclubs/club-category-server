from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from community.apps.emojis.models import PostEmoji
from community.modules.producers.post_emojis import PostEmojiProducer


# Main Section
@receiver(pre_save, sender=PostEmoji)
def post_emoji_pre_save(sender, instance, *args, **kwargs):
    print("========== PostEmoji pre_save ==========")

    if not instance.id:
        instance._is_changed = False
    else:
        _instance = PostEmoji.objects.filter(id=instance.id).first()
        instance._is_changed = _instance.emoji_code != instance.emoji_code


@receiver(post_save, sender=PostEmoji)
def sync_post_emoji_post_save(sender, instance, created, **kwargs):
    print("========== PostEmoji post_save : Sync ==========")
    is_changed = instance._is_changed

    if created or is_changed:
        PostEmojiProducer().sync_post_emoji(instance)


@receiver(post_save, sender=PostEmoji)
def count_post_emoji_post_save(sender, instance, created, **kwargs):
    print("========== PostEmoji post_save : Count ==========")

    post = instance.post
    profile = instance.profile
    is_changed = instance._is_changed

    if created or is_changed:
        # Post PostEmoji Count
        post.update_post_emoji_count()

        # Profile PostEmoji Count
        profile.update_profile_posts_emoji_count()


@receiver(post_delete, sender=PostEmoji)
def post_emoji_post_delete(sender, instance, *args, **kwargs):
    print("========== PostEmoji post_delete ==========")
    # 1. 카운트 감소.
    # 2. post 서버 PostEmoji 삭제 sync

    post = instance.post

    # Post PostEmoji Count
    post.update_post_emoji_count()

    # Profile PostEmoji Count
    instance.profile.update_profile_posts_emoji_count()

    PostEmojiProducer().delete_post_emoji(instance)
