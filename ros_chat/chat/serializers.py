from rest_framework import serializers
from .models import Chat, Message
from accounts.serializers import UserSerializer


class ChatRoomSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    class Meta:
        model = Chat
        fields = ('id', 'name', 'participants', 'created_at')


class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ('id', 'chat', 'user', 'content', 'timestamp')