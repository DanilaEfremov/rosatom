from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view

from .models import Chat
from .forms import MessageForm


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
def chat_htmx_detail(request, chat_id: int):
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
    form = MessageForm()
    template = 'chat/chat_detail_htmx.html' if not request.htmx else 'chat/part/chat_detail_content_htmx.html'
    return render(request, template, {'chat': chat, 'messages': messages, 'form': form})



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
