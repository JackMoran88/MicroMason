from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .serializers import *
from product.serializers import *


class NotificationConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()


    async def notify(self, event):
        await self.send_json(event["content"])


    async def receive_json(self, content, **kwargs):
        groups = self.get_groups(data=content['data'])
        if not groups:
            return

        for group in groups:
            await self.channel_layer.group_add(
                group,
                self.channel_name,
            )

    def get_groups(self, *args, **kwargs):
        groups_name = []
        if 'Categories' in kwargs['data']:
            groups_name.append(CategoriesListSerializer().get_group_name())

        if 'Product' in kwargs['data']:
            groups_name.append(ProductDetailSerializer().get_group_name())

        return groups_name

