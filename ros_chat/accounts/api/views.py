from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework import status

from .serializers import UserSerializer
from accounts.models import CustomUser


@api_view(['POST'])
def register(request):
    """Производит регистрацию нового пользователя

        Args:
            request (HttpRequest): Запрос.
        Returns:
            Сообщение в формате JSON
        """
    username = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email")
    if not username or not password:
        return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)
    user = CustomUser.objects.create_user(username=username, password=password, email=email)
    user.save()
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key, 'user': UserSerializer(user).data}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login(request):
    """Производит аутентификацию

    Args:
        request (HttpRequest): Запрос.
    Returns:
        Сообщение в формате JSON
    """
    from django.contrib.auth import authenticate
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(username=username, password=password)
    if not user:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key}, status=status.HTTP_200_OK)