# chat/consumers.py
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from accounts.models import CustomUser
from .models import Chat, Message
import json

class ChatJsonConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = f'chat_{self.chat_id}'

        # Присоединяемся к группе
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Покидаем группу
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive_json(self, content, **kwargs):
        message = content.get('message')
        if message is None:
            return
        message = message.strip()

        # Получение пользователя в асинхронном контексте
        user = self.scope['user']

        chat = await Chat.objects.aget(id=self.chat_id)
        await Message.objects.acreate(chat=chat, user=user, content=message)

        # Отправляем сообщение в группу
        await self.channel_layer.group_send(self.room_group_name, {
        # An event has a special 'type' key corresponding to the name of the method
        # that should be invoked on consumers that receive the event.
            'type': 'chat_message',
            'message': message,
            'username': user.username,
        })


    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        # Отправка сообщения через WebSocket
        await self.send_json(content={'message': message, 'username': username})

