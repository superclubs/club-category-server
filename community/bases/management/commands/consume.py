import asyncio

from django.core.management.base import BaseCommand

from community.apps.bans.services.consumer import BanConsumerService
from community.apps.friends.services.consumer import (
    FriendConsumerService,
    FriendRequestConsumerService,
)
from community.apps.users.services import UserConsumerService


# Main Section
class Command(BaseCommand):
    help = "Consume messages"

    consumers = [
        BanConsumerService,
        FriendRequestConsumerService,
        FriendConsumerService,
        UserConsumerService,
    ]

    def handle(self, *args, **options):
        asyncio.run(self.handle_async(*args, **options))

    async def handle_async(self, *args, **kwargs):
        await asyncio.gather(*[consumer().consume_messages() for consumer in self.consumers])
