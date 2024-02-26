# Django
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

# Base
from config.settings.base import SUPERCLUB_WEB_HOST

# Serializers
from community.apps.users.api.serializers import UserProfileSerializer
from community.apps.profiles.api.serializers import ProfileSerializer

# Models
from community.apps.posts.models import Post
from community.apps.badges.models import Badge


# Main Section
@receiver(pre_save, sender=Post)
def post_pre_save_sync_post(sender, instance, *args, **kwargs):
    print('========== Post pre_save: Sync Post ==========')
    if instance.id is None:
        if instance.user:
            instance.user_data = UserProfileSerializer(instance=instance.user).data
        if instance.profile:
            instance.profile_data = ProfileSerializer(instance=instance.profile).data
    # else:
    #     _instance = Post.available.filter(id=instance.id).first()
    #     if _instance:
    #         for field in [
    #             # Main
    #             'content_summary', 'public_type', 'password', 'reserved_at', 'boomed_at', 'point',
    #
    #             # Count
    #             'comment_count', 'total_like_count', 'dislike_count',
    #
    #             # Boolean
    #             'password',
    #             'is_active', 'is_notice', 'is_event', 'is_temporary', 'is_secret',
    #             'is_search', 'is_share', 'is_comment', 'is_reserved', 'is_boomed', 'is_vote',
    #
    #             # Date
    #             'achieved_20_points_at',
    #         ]:
    #             _value = getattr(_instance, field)
    #             value = getattr(instance, field)
    #
    #             if _value != value:
    #                 print('========================= sync_post_task =========================')
    #                 try:
    #                     sync_post_task.apply_async((instance.id,), countdown=2)
    #                 except:
    #                     pass


@receiver(post_save, sender=Post)
def post_post_save_create_new_post_badge(sender, instance, created, **kwargs):
    print('========== Post post_save : Create New Post Badge ==========')
    if created:
        if not instance.is_temporary and not instance.is_agenda:
            new_post_badge = Badge.available.get(title='New', model_type='POST')
            instance.badges.add(new_post_badge.id)


@receiver(post_save, sender=Post)
def post_post_save_set_web_url(sender, instance, created, **kwargs):
    print('========== Post post_save: Set Field ==========')

    if created:
        if not instance.is_temporary:
            instance.web_url = SUPERCLUB_WEB_HOST + f'/community/{instance.community.id}/post/{instance.id}'

# @receiver(post_save, sender=Post)
# def post_post_save(sender, instance, created, **kwargs):
#     print('========================= Post post_save: Sync Post =========================')
#     if created and not instance.is_default and not instance.is_temporary and not instance.is_reserved and \
#         instance.public_type != 'ONLY_ME':
#         sync_post_task.apply_async((instance.id,), countdown=2)
