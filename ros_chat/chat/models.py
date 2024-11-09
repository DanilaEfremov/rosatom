from django.db import models
from django.utils import timezone

from accounts.models import CustomUser

class Chat(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    participants = models.ManyToManyField(CustomUser, related_name='chats')

    def __str__(self):
        return self.name


class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name="messages", on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Message from {self.user.username} in {self.chat.name}'
