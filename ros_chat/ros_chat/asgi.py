import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ros_chat.settings')  # Замените your_project_name на реальное имя вашего проекта

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
})
