from django.db import models
from advert.models import Advert
from user.models import CustomUser


class Inbox(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name='receiver', on_delete=models.CASCADE)
    advert = models.ForeignKey(Advert, on_delete=models.CASCADE)

class Message(models.Model):
    inbox = models.ForeignKey(Inbox, related_name='message', on_delete=models.CASCADE)
    sender = models.ForeignKey(CustomUser, related_name='message_sender', on_delete=models.CASCADE)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
