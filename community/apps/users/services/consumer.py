import json
from asgiref.sync import sync_to_async
from model_utils import Choices

from community.apps.users.api.serializers import UserSyncSerializer
from community.apps.users.models import User
from community.bases.kafka import KafkaConsumerService


# Main Section
class UserConsumerService(KafkaConsumerService):
    action_choices = Choices(
        ("SYNC", "SYNC"),
    )

    def __init__(self):
        super().__init__(topic="users")

    def __parse_msg(self, msg):
        msg_value = json.loads(msg.value)
        action = msg_value.get("action")
        data = msg_value.get("data", None)
        return action, data

    async def process_message(self, msg):
        action, data = self.__parse_msg(msg)

        if action == self.action_choices.SYNC:
            await self.sync(data)

        print(f"processed complete topic: {msg.topic}, action: {action}, data: {data}")

    @sync_to_async
    def sync(self, data: dict):
        id = data.pop("id", None)
        if not id:
            return

        if instance := User.objects.filter(id=id).first():
            serializer = UserSyncSerializer(instance=instance, data=data, partial=True)
        else:
            serializer = UserSyncSerializer(data=data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
