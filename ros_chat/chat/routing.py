from django.urls import path
from . import consumers, ws_api_consumers, ws_htmx_consumer
from channels.auth import AuthMiddlewareStack
from .middleware.drf import DRFAuthTokenMiddleware


websocket_urlpatterns = [
    path('ws/chat/<int:chat_id>/', AuthMiddlewareStack(consumers.ChatConsumer.as_asgi())),
    path('ws/htmx_chat/<int:chat_id>/', AuthMiddlewareStack(ws_htmx_consumer.ChatConsumer.as_asgi())),
    path('ws/api/chat/<int:chat_id>/', DRFAuthTokenMiddleware(ws_api_consumers.ChatJsonConsumer.as_asgi())),
]
