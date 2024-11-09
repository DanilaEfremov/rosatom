from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from accounts.models import CustomUser
from chat.models import Chat, Message
from .serializers import MessageSerializer, ChatRoomSerializer



#### Rest API Views
@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def messages(request, chat_id):
    """Запрос на получение списка сообщений в чате или отправку нового
        Args:
            request (HttpRequest): Запрос.
            chat_id (int): ID чата
        Returns:
            Сообщение в формате JSON
    """

    user = request.user
    chat_room = get_object_or_404(Chat, id=chat_id)
    if request.method == 'POST':
        content = request.data.get("content")
        if not content:
            return Response({"error": "Message cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)
        if user not in chat_room.participants.all():
            return Response({"error": "You do not have access to this chat room"}, status=status.HTTP_403_FORBIDDEN)
        message = Message.objects.create(user=user, chat=chat_room, content=content)
        data = MessageSerializer(message).data
        return Response(data, status=status.HTTP_201_CREATED)
    elif request.method == 'GET':
        if user not in chat_room.participants.all():
            return Response({"error": "You do not have access to this chat room"}, status=status.HTTP_403_FORBIDDEN)
        messages = chat_room.messages.all()
        return Response(MessageSerializer(messages, many=True).data, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_chats(request):
    """Производит получение списка чатов
        Args:
            request (HttpRequest): Запрос.
        Returns:
            Сообщение в формате JSON
        """

    user = request.user
    chats = Chat.objects.filter(participants=user)
    if user.is_superuser:
        chats = Chat.objects.all()
    serialized_chats = ChatRoomSerializer(chats, many=True).data
    return Response(serialized_chats, status=status.HTTP_200_OK)



@api_view(['DELETE', 'PUT'])
@permission_classes([IsAuthenticated])
def move_user_in_chat(request, chat_id, user_id):
    """Производит добавление или удаление пользователя из чата

        Args:
            request (HttpRequest): Запрос.
            chat_id (int): ID чата
            user_id (int): ID пользователя
        Returns:
            Сообщение в формате JSON
        """
    if not request.user.is_superuser:
        return Response({"error": "You do not have permission to perform this action"},
                        status=status.HTTP_403_FORBIDDEN)
    try:
        chat = Chat.objects.get(id=chat_id)
    except Chat.DoesNotExist:
        return Response({"error": "Chat not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        try:
            user_to_remove = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if user_to_remove not in chat.participants.all():
            return Response({"error": "User is not a participant in this chat"}, status=status.HTTP_400_BAD_REQUEST)

        chat.participants.remove(user_to_remove)

        return Response({"message": f"User {user_to_remove.username} removed from chat"}, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        try:
            user_to_add = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if user_to_add in chat.participants.all():
            return Response({"error": "User is already a participant in this chat"}, status=status.HTTP_400_BAD_REQUEST)

        chat.participants.add(user_to_add)

        return Response({"message": f"User {user_to_add.username} added to chat"}, status=status.HTTP_200_OK)