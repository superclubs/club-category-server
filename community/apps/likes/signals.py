# Django
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from community.apps.likes.constants.index import emoji_dict
# Models
from community.apps.likes.models import PostDislike, PostLike

# Tasks
from community.apps.likes.tasks import sync_dislike_task, sync_like_task
from community.apps.profiles.api.serializers import ProfileSerializer

# Serializers
from community.apps.users.api.serializers import UserSerializer


# Main Section
@receiver(pre_save, sender=PostLike)
def post_like_pre_save(sender, instance, *args, **kwargs):
    print("========== PostLike pre_save: Sync Post Like ==========")
    if not instance.id:
        instance.user_data = UserSerializer(instance=instance.user).data
        instance.profile_data = ProfileSerializer(instance=instance.profile).data
        instance._is_changed = False
    else:
        _instance = PostLike.objects.filter(id=instance.id).first()
        instance._is_changed = _instance.type != instance.type or _instance.is_active != instance.is_active


@receiver(post_save, sender=PostLike)
def post_like_post_save(sender, instance, created, **kwargs):
    print("========== PostLike pre_save: Sync Post Like ==========")

    post = instance.post
    user = instance.user

    is_changed = instance._is_changed

    if created or is_changed:
        post.update_post_total_like_count()
        sync_like_task.apply_async((instance.id,), countdown=1)

    emoji_code = emoji_dict.get(instance.type)
    if created or (is_changed and instance.is_active):
        # 좋아요 시 emoji 생성/수정
        try:
            post.emoji_post(user, emoji_code)
        except Exception as e:
            print(f"Postlike 생성 {e}")

    elif is_changed and not instance.is_active:
        try:
            # 좋아요 취소 시 emoji 삭제
            post.unemoji_post(user, emoji_code)
        except Exception as e:
            print(f"Postlike 취소 {e}")


@receiver(pre_save, sender=PostDislike)
def post_dislike_pre_save(sender, instance, *args, **kwargs):
    print("========== PostDislike pre_save: Sync Post Dislike ==========")
    # Synchronize DisLike
    if not instance.id:
        instance._is_changed = False
    else:
        _instance = PostDislike.objects.filter(id=instance.id).first()
        instance._is_changed = _instance.is_active != instance.is_active


@receiver(post_save, sender=PostDislike)
def post_dislike_post_save(sender, instance, created, **kwargs):
    print("========== PostDislike post_save: Sync Post DisLike ==========")

    is_changed = instance._is_changed
    if created or is_changed:
        instance.post.update_post_dislike_count()
        sync_dislike_task.apply_async((instance.id,), countdown=1)
