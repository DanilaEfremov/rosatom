# chat/consumers.py
import json
import logging

from channels.generic.websocket import AsyncWebsocketConsumer
from django.template.loader import render_to_string

from accounts.models import CustomUser
from accounts.views import login
from .models import Chat, Message
from core.utils import convertDatetimeToString


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = f'chat_{self.chat_id}'
        # Присоединяемся к группе
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        logging.info(f'{self.scope["user"]} is connected to chat {self.chat_id}')

    async def disconnect(self, close_code):
        # Покидаем группу
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['chat_message'].strip()

        # Получение пользователя в асинхронном контексте
        user = self.scope['user']
        chat = await Chat.objects.aget(id=self.chat_id)
        if message == '':
            return
        msg_record = await Message.objects.acreate(chat=chat, user=user, content=message)
        context = {
            'type'      : 'chat_message',
            'message'   : message,
            'username'  : user.username,
            'first_name': user.first_name,
            'last_name' : user.last_name,
            'timestamp' : convertDatetimeToString(msg_record.timestamp),
        }
        # # Отправляем сообщение в группу
        await self.channel_layer.group_send(self.room_group_name, context)

    async def chat_message(self, event):
        context = {
            'message'   : event['message'],
            'username'  : event['username'],
            'first_name': event['first_name'],
            'last_name' : event['last_name'],
            'timestamp' : event['timestamp'],
            'is_my_msg' : event['username'] == self.scope['user'].username
        }
        logging.info(context)
        # Отправка сообщения через WebSocket
        await self.send(text_data=render_to_string('chat/part/chat_message_htmx.html', context=context))
