# chat/consumers.py
import json
import logging

from channels.generic.websocket import AsyncJsonWebsocketConsumer

from accounts.models import CustomUser
from .models import Chat, Message
from core.utils import convertDatetimeToString

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
        msg_record = await Message.objects.acreate(chat=chat, user=user, content=message)
        context = {
            'type':      'chat_message',
            'message':    message,
            'username':   user.username,
            'first_name': user.first_name,
            'last_name':  user.last_name,
            'timestamp':  convertDatetimeToString(msg_record.timestamp),
        }
        # Отправляем сообщение в группу
        await self.channel_layer.group_send(self.room_group_name, context)


    @classmethod
    async def encode_json(cls, content):
        return json.dumps(content, ensure_ascii=False)

    async def chat_message(self, event):
        context = {
            'message'   : event['message'],
            'username'  : event['username'],
            'first_name': event['first_name'],
            'last_name' : event['last_name'],
            'timestamp' : event['timestamp']
        }

        # Отправка сообщения через WebSocket
        await self.send_json(content=context)

