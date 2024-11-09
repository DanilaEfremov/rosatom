from django.urls import path
from channels.auth import AuthMiddlewareStack
from .middleware.drf import DRFAuthTokenMiddleware

from . import ws_api_consumers, ws_htmx_consumer


websocket_urlpatterns = [
    path('ws/htmx_chat/<int:chat_id>/', AuthMiddlewareStack(ws_htmx_consumer.ChatConsumer.as_asgi())),
    path('ws/api/chat/<int:chat_id>/', DRFAuthTokenMiddleware(ws_api_consumers.ChatJsonConsumer.as_asgi())),
]
