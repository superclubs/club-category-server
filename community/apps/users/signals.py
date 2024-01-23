# Django
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

# DRF
from rest_framework.authtoken.models import Token

# Tasks
from community.apps.users.tasks import sync_user_task

# Models
from community.apps.users.models import User


# Main Section
@receiver(post_save, sender=User)
def create_token(sender, instance, created, **kwargs):
    print('========== User post_save: Create Token ==========')

    if created:
        # Create Token
        Token.objects.create(user=instance)


@receiver(pre_save, sender=User)
def sync_user(sender, instance, **kwargs):
    print('========== User pre_save: Sync User ==========')

    if instance.id is None:  # new object will be created
        pass  # write your code here
    else:
        _instance = User.available.filter(id=instance.id).first()
        if _instance:
            for field in ['username', 'badge_image_url', 'banner_image_url', 'profile_image_url', 'status',
                          'ring_color']:
                _value = getattr(_instance, field)
                value = getattr(instance, field)

                if _value != value:
                    print('========== sync_user_task ==========')
                    sync_user_task.delay(instance.id)
                    break
