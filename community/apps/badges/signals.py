# Django
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

# Models
from community.apps.badges.models import Badge


# Main Section
@receiver(pre_save, sender=Badge)
def cache_image(sender, instance, *args, **kwargs):
    print('========== Badge pre_save: Image ==========')

    image = None

    if instance.id:
        badge = Badge.available.get(id=instance.id)
        image = badge.image

    instance.__image = image


@receiver(post_save, sender=Badge)
def image_update(sender, instance, created, **kwargs):
    print('========== Badge post_save: Image ==========')

    if instance.__image != instance.image:

        # Update Image
        if instance.image:
            instance.image_url = instance.image.url
            instance.save(update_fields=['image_url'])
