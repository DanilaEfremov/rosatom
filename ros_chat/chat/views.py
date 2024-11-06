from crypt import methods
from lib2to3.fixes.fix_input import context

from django.http import HttpResponseForbidden, HttpResponseNotAllowed, Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated

from accounts.models import CustomUser
from .models import Chat, Message
from .forms import MessageForm

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .serializers import MessageSerializer, ChatRoomSerializer


#### Web App Views
@login_required
@api_view(['GET'])
def chat_list(request):
    """Возвращает список чатов пользователя."""
    chats = Chat.objects.all() if request.user.is_superuser else request.user.chats.all()
    template = 'chat/part/chat_list_content.html' if request.htmx else 'chat/chat_list.html'
    return render(request, template, {'chats': chats})


@login_required
@api_view(['GET'])
def chat_detail(request, chat_id: int):
    """Возвращает страницу с конкретным чатом.

    Args:
        request (HttpRequest): Запрос.
        chat_id (int): ID чата.
    """
    try:
        chat = get_object_or_404(Chat, id=chat_id)
    except Http404:
        return render(request, 'chat/chat_not_found.html', context={'chat_id': chat_id})


    if request.user not in chat.participants.all() and not request.user.is_superuser:
        return render(request, 'chat/chat_forbidden.html', context={'chat_id': chat_id})

    messages = chat.messages.all().order_by('timestamp')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat = chat
            message.user = request.user
            message.save()
            return redirect('chat_detail', chat_id=chat.id)
    else:
        form = MessageForm()

    return render(request, 'chat/chat_detail.html', {
        'chat': chat,
        'messages': messages,
        'form': form
    })


@login_required
@api_view(['DELETE'])
def chat_unsubscribe(request, chat_id: int):
    """Отписывает пользователя от чата.

    Args:
        request (HttpRequest): Запрос.
        chat_id (int): ID чата.
    """

    try:
        chat = get_object_or_404(Chat, id=chat_id)
    except Http404:
        return render(request, 'chat/chat_not_found.html', context={'chat_id': chat_id})


    if request.user not in chat.participants.all() and not request.user.is_superuser:
        return render(request, 'chat/chat_forbidden.html', context={'chat_id': chat_id})
    chat.participants.remove(request.user)
    chats = Chat.objects.all() if request.user.is_superuser else request.user.chats.all()
    return render(request, 'chat/part/chat_list.html', {'chats': chats})




#### Rest API Views
@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def messages(request, chat_id):
    user = request.user
    chat_room = get_object_or_404(Chat, id=chat_id)
    if request.method == 'POST':
        content = request.data.get("content")

        if not content:
            return Response({"error": "Message cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)

        if user not in chat_room.participants.all():
            return Response({"error": "You do not have access to this chat room"}, status=status.HTTP_403_FORBIDDEN)

        message = Message.objects.create(user=user, chat=chat_room, content=content)
        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)

    elif request.method == 'GET':
        if user not in chat_room.participants.all():
            return Response({"error": "You do not have access to this chat room"}, status=status.HTTP_403_FORBIDDEN)
        messages = chat_room.messages.all()
        return Response(MessageSerializer(messages, many=True).data, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_chats(request):
    user = request.user

    chats = Chat.objects.filter(participants=user)

    if user.is_superuser:
        chats = Chat.objects.all()

    serialized_chats = ChatRoomSerializer(chats, many=True).data
    return Response(serialized_chats, status=status.HTTP_200_OK)



@api_view(['DELETE', 'PUT'])
@permission_classes([IsAuthenticated])
def remove_user_from_chat(request, chat_id, user_id):
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