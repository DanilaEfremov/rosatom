from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """На всякий случай делаем свой класс пользователя.
    Он может пригодиться в дальнейшем.
    Не забываем сообщить об этом системе,
    добавив строчку AUTH_USER_MODEL = 'accounts.CustomUser' в файл настроек.
    """

    @property
    def full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'.strip()

    @property
    def nickname(self) -> str:
        return self.username

    def __str__(self):
        return self.full_name if self.full_name != '' else self.nickname
