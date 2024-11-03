import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ros_chat.settings')
django.setup()
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing
from channels.security.websocket import AllowedHostsOriginValidator


application = ProtocolTypeRouter(
    {
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        URLRouter(chat.routing.websocket_urlpatterns)
        )
    }
)
