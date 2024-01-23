# Django
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

# Models
from community.apps.comments.models import Comment


# Main Section
@receiver(pre_save, sender=Comment)
def cache_image(sender, instance, *args, **kwargs):
    print('========== Comment pre_save: Image ==========')
    image = None

    if instance.id:
        comment = Comment.available.get(id=instance.id)
        image = comment.image

    instance.__image = image


@receiver(post_save, sender=Comment)
def image_update(sender, instance, created, **kwargs):
    print('========== Comment post_save: Image ==========')
    if instance.__image != instance.image:

        # Update Image
        if instance.image:
            instance.image_url = instance.image.url
            instance.save(update_fields=['image_url'])
