import asyncio

from model_utils import Choices

from community.bases.kafka import KafkaProducerService


class BookmarkProducer(KafkaProducerService):
    action_choices = Choices(
        ("CREATE", "CREATE"),
        ("DELETE", "DELETE"),
    )

    def __init__(self):
        super().__init__(topic="bookmark")

    def __produce(self, action: str, data: dict):
        message = dict(action=action, data=data)
        asyncio.run(self.send_messages([message]))

    def create_bookmark(self, instance):
        from community.apps.bookmarks.api.serializers import (
            PostBookmarkCreateSyncSerializer,
        )
        from community.apps.bookmarks.models import PostBookmark

        action = self.action_choices.CREATE
        if isinstance(instance, PostBookmark):
            data = PostBookmarkCreateSyncSerializer(instance=instance).data
        else:
            return
        self.__produce(action, data)

    def delete_bookmark(self, instance):
        from community.apps.bookmarks.api.serializers import (
            PostBookmarkBaseSyncSerializer,
        )
        from community.apps.bookmarks.models import PostBookmark

        action = self.action_choices.DELETE
        if isinstance(instance, PostBookmark):
            data = PostBookmarkBaseSyncSerializer(instance=instance).data
        else:
            return
        self.__produce(action, data)
