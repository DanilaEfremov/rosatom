from django.urls import path
from . import views


urlpatterns = [
    path('', views.get_chats, name='api_chat_list'),
    path('<int:chat_id>/message/', views.messages, name='api_chat_messages'),
    path('<int:chat_id>/user/<int:user_id>', views.move_user_in_chat, name='api_chat_users'),
]
