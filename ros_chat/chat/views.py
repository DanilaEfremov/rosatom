from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Chat, Message
from .forms import MessageForm


@login_required
def chat_list(request):
    if request.user.is_superuser:
        chats = Chat.objects.all()
    else:
        chats = request.user.chats.all()

    return render(request, 'chat/chat_list.html', {'chats': chats})

@login_required
def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)

    if request.user not in chat.participants.all() and not request.user.is_superuser:
        return HttpResponseForbidden("У вас нет доступа к этому чату.")

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
