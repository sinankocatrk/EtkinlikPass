from django.db import models
from advert.models import Advert
from user.models import CustomUser


class Inbox(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name='receiver', on_delete=models.CASCADE)
    advert = models.ForeignKey(Advert, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_message = models.ForeignKey('Message', related_name='last_message', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.sender.username} - {self.receiver.username} for {self.advert.event.title}"

class Message(models.Model):
    inbox = models.ForeignKey(Inbox, related_name='message', on_delete=models.CASCADE)
    sender = models.ForeignKey(CustomUser, related_name='message_sender', on_delete=models.CASCADE)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} to: {self.inbox.sender.username} - {self.inbox.receiver.username} for {self.inbox.advert.event.title}"
