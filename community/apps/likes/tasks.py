# Django
from celery import shared_task

# Gateway
from community.modules.gateways.post import gateway as gateway_post


@shared_task(name='sync_like_task', bind=True)
def sync_like_task(self, instance_id):
    print('========================= Like: sync_like_task =========================')

    from community.apps.likes.models import PostLike
    from community.apps.likes.api.serializers import PostLikeSyncSerializer

    instance = PostLike.available.filter(id=instance_id).first()
    if not instance:
        return

    data = PostLikeSyncSerializer(instance=instance).data

    # API Gateway
    response = gateway_post.sync_like(data)
    print('response : ', response)


@shared_task(name='sync_dislike_task', bind=True)
def sync_dislike_task(self, instance_id):
    print('========================= Dislike: sync_dislike_task =========================')

    from community.apps.likes.models import PostDislike
    from community.apps.likes.api.serializers import PostDislikeSyncSerializer

    instance = PostDislike.available.filter(id=instance_id).first()
    if not instance:
        return

    data = PostDislikeSyncSerializer(instance=instance).data

    # API Gateway
    response = gateway_post.sync_dislike(data)
    print('response : ', response)
