import json

from asgiref.sync import sync_to_async
from model_utils import Choices

from community.apps.bans.api.serializers import (
    UserBanCreateSerializer,
    UserBanSyncSerializer,
)
from community.apps.bans.models import UserBan
from community.bases.kafka import KafkaConsumerService


# Main Section
class BanConsumerService(KafkaConsumerService):
    action_choices = Choices(
        ("SYNC", "SYNC"),
        ("CREATE", "CREATE"),
    )

    def __init__(self):
        super().__init__(topic="ban")

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

        print(f"processed complete topic: {msg.topic}, action: {action}, data: {data}")

    @sync_to_async
    def create(self, data: dict):
        id = data.get("id", None)
        if not id:
            return
        instance = UserBan.objects.filter(id=id).first()
        if instance:
            return
        serializer = UserBanCreateSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

    @sync_to_async
    def sync(self, data: dict):
        id = data.pop("id", None)
        if not id:
            return

        instance = UserBan.objects.filter(id=id).first()
        if not instance:
            return

        serializer = UserBanSyncSerializer(instance=instance, data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
