from django.urls import path
from . import consumers, ws_api_consumers
from channels.auth import AuthMiddlewareStack
from .middleware.drf import DRFAuthTokenMiddleware


websocket_urlpatterns = [
    path('ws/chat/<int:chat_id>/', AuthMiddlewareStack(consumers.ChatConsumer.as_asgi())),
    path('ws/api/chat/<int:chat_id>/', DRFAuthTokenMiddleware(ws_api_consumers.ChatJsonConsumer.as_asgi())),
]
