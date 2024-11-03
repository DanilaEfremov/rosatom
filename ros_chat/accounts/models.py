from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):

    @property
    def full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'.strip()

    @property
    def nickname(self) -> str:
        return self.username

    def __str__(self):
        return self.full_name if self.full_name != '' else self.nickname
