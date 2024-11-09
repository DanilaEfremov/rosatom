from django.contrib import admin

from .models import Chat, Message

# Регистрация модели Chat
@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    filter_horizontal = ('participants',)

# Регистрация модели Message
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('chat', 'user', 'content', 'timestamp')
    list_filter = ('chat', 'user')
    search_fields = ('content',)