import asyncio

from model_utils import Choices

from community.apps.emojis.api.serializers import (
    PostEmojiDeleteSyncSerializer,
    PostEmojiSyncSerializer,
)
from community.apps.emojis.models import PostEmoji
from community.bases.kafka import KafkaProducerService


class PostEmojiProducer(KafkaProducerService):
    action_choices = Choices(
        ("SYNC", "SYNC"),
        ("DELETE", "DELETE"),
    )

    def __init__(self):
        super().__init__(topic="post_emojis")

    def __produce(self, action: str, data: dict):
        message = dict(action=action, data=data)
        asyncio.run(self.send_messages([message]))

    def sync_post_emoji(self, instance: PostEmoji):
        action = self.action_choices.SYNC
        data = PostEmojiSyncSerializer(instance=instance).data
        self.__produce(action, data)

    def delete_post_emoji(self, instance: PostEmoji):
        action = self.action_choices.DELETE
        data = PostEmojiDeleteSyncSerializer(instance=instance).data
        self.__produce(action, data)
