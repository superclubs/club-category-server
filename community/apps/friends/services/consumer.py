# Third Party
import json

from asgiref.sync import sync_to_async
from model_utils import Choices

from community.apps.friends.api.serializers.create import (
    FriendCreateSerializer,
    FriendRequestCreateSerializer,
)
from community.apps.friends.api.serializers.index import (
    FriendRequestSyncSerializer,
    FriendSyncSerializer,
)
from community.apps.friends.models.index import Friend, FriendRequest

# Bases
from community.bases.kafka import KafkaConsumerService


# Main Section
class FriendConsumerService(KafkaConsumerService):
    action_choices = Choices(
        ("SYNC", "SYNC"),
        ("CREATE", "CREATE"),
        ("DELETE", "DELETE"),
    )

    def __init__(self):
        super().__init__(topic="friends")

    def __parse_msg(self, msg):
        msg_value = json.loads(msg.value)
        action = msg_value.get("action")
        data = msg_value.get("data", None)
        return action, data

    async def process_message(self, msg):
        action, data = self.__parse_msg(msg)

        if action == self.action_choices.SYNC:
            await self.sync(data)
        elif action == self.action_choices.CREATE:
            await self.create(data)
        elif action == self.action_choices.DELETE:
            await self.delete(data)

        print(f"processed complete topic: {msg.topic}, action: {action}, data: {data}")

    @sync_to_async
    def create(self, data: dict):
        id = data.get("id", None)
        if not id:
            return
        instance = Friend.objects.filter(id=id).first()
        if instance:
            return
        serializer = FriendCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

    @sync_to_async
    def delete(self, data: dict):
        if id := data.get("id", None):
            Friend.objects.filter(id=id).delete()

    @sync_to_async
    def sync(self, data: dict):
        id = data.pop("id", None)
        if not id:
            return

        instance = Friend.objects.filter(id=id).first()
        if not instance:
            return

        serializer = FriendSyncSerializer(instance=instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()


class FriendRequestConsumerService(KafkaConsumerService):
    action_choices = Choices(
        ("SYNC", "SYNC"),
        ("CREATE", "CREATE"),
        ("DELETE", "DELETE"),
    )

    def __init__(self):
        super().__init__(topic="friend_requests")

    def __parse_msg(self, msg):
        msg_value = json.loads(msg.value)
        action = msg_value.get("action")
        data = msg_value.get("data", None)
        return action, data

    async def process_message(self, msg):
        action, data = self.__parse_msg(msg)

        if action == self.action_choices.SYNC:
            await self.sync(data)
        elif action == self.action_choices.CREATE:
            await self.create(data)
        elif action == self.action_choices.DELETE:
            await self.delete(data)

        print(f"processed complete topic: {msg.topic}, action: {action}, data: {data}")

    @sync_to_async
    def create(self, data: dict):
        id = data.get("id", None)
        if not id:
            return
        instance = FriendRequest.objects.filter(id=id).first()
        if instance:
            return
        serializer = FriendRequestCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return serializer.data

    @sync_to_async
    def delete(self, data: dict):
        if id := data.get("id", None):
            FriendRequest.objects.filter(id=id).delete()
            return id

    @sync_to_async
    def sync(self, data: dict):
        id = data.pop("id", None)
        if not id:
            return

        instance = FriendRequest.objects.filter(id=id).first()
        if not instance:
            return

        serializer = FriendRequestSyncSerializer(instance=instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
