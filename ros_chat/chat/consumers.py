# chat/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer

from accounts.models import CustomUser
from .models import Chat, Message
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = f'chat_{self.chat_id}'

        # Присоединяемся к группе
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Покидаем группу
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message'].strip()
        user_id = text_data_json['user_id']

        # Получение пользователя в асинхронном контексте
        user = self.scope['user']

        chat = await Chat.objects.aget(id=self.chat_id)
        if message == '':
            return
        await Message.objects.acreate(chat=chat, user=user, content=message)

        # Отправляем сообщение в группу
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': user.username,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Отправка сообщения через WebSocket
        await self.send(text_data=json.dumps({'message': message, 'username': username}))