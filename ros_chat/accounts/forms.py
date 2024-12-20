from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    """
    Пользовательская форма регистрации
    """
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'username', 'email')
