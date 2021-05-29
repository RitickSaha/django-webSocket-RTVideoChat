from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio

import datetime


class VideoRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.group_name = 'video_%s' % self.room_name

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "tester",
                'tester': '1'
            }
        )

    async def tester(self, event):
        tester = event['tester']
        await self.send(text_data=json.dumps({
            "tester": tester,
        }))
    async def receive(self, text_data):
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'tester',
                'tester': text_data
            }
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
    pass
