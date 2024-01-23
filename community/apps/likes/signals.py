# Django
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

# Models
from community.apps.likes.models import PostLike, PostDislike

# Serializers
from community.apps.users.api.serializers import UserSerializer
from community.apps.profiles.api.serializers import ProfileSerializer

# Tasks
from community.apps.likes.tasks import sync_like_task, sync_dislike_task


# Main Section
@receiver(pre_save, sender=PostLike)
def post_like_pre_save(sender, instance, *args, **kwargs):
    print('========== PostLike pre_save: Sync Post Like ==========')
    # Initialize Like
    if instance.id is None:
        instance.user_data = UserSerializer(instance=instance.user).data
        instance.profile_data = ProfileSerializer(instance=instance.profile).data

    # Synchronize Like
    else:
        _instance = PostLike.available.filter(id=instance.id).first()
        if _instance:
            for field in [
                # Main
                'type',

                # Boolean
                'is_active',
            ]:
                _value = getattr(_instance, field)
                value = getattr(instance, field)

                if _value != value:
                    sync_like_task.apply_async((instance.id,), countdown=1)
                    break


@receiver(post_save, sender=PostLike)
def post_like_post_save(sender, instance, created, **kwargs):
    print('========== PostLike pre_save: Sync Post Like ==========')

    if created:
        sync_like_task.apply_async((instance.id,), countdown=1)


@receiver(pre_save, sender=PostDislike)
def post_dislike_pre_save(sender, instance, *args, **kwargs):
    print('========== PostDislike pre_save: Sync Post Dislike ==========')
    # Synchronize DisLike
    if instance.id is not None:
        _instance = PostDislike.available.filter(id=instance.id).first()
        if _instance:
            for field in [
                # Boolean
                'is_active',
            ]:
                _value = getattr(_instance, field)
                value = getattr(instance, field)

                if _value != value:
                    sync_dislike_task.apply_async((instance.id,), countdown=1)
                    break


@receiver(post_save, sender=PostDislike)
def post_dislike_post_save(sender, instance, created, **kwargs):
    print('========== PostDislike post_save: Sync Post DisLike ==========')

    if created:
        sync_dislike_task.apply_async((instance.id,), countdown=1)
