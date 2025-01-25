# chat/consumers.py
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

# Rewrite Chat Server as Asynchronous
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # self.accept()
        
        # after having channel layer
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group

        # async_to_sync(self.channel_layer.group_add)(
        #     self.room_group_name, self.channel_name
        # )

        # self.accept()

        # Rewrite Chat Server as Asynchronous
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # after having channel layer

        # Leave room group

        # async_to_sync(self.channel_layer.group_discard)(
        #     self.room_group_name, self.channel_name
        # )

        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        # text_data_json = json.loads(text_data)
        # message = text_data_json["message"]

        # self.send(text_data=json.dumps({"message": message}))

        # after having channel layer
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group

        # async_to_sync(self.channel_layer.group_send)(
        #     self.room_group_name, {"type": "chat.message", "message": message}
        # )

        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message}
        )
    
    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket

        # self.send(text_data=json.dumps({"message": message}))

        await self.send(text_data=json.dumps({"message": message}))