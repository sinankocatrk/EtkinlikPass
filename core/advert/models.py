from django.db import models
from event.models import Event
from user.models import CustomUser as User 

class Advert(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='adverts', null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    price = models.IntegerField(null=True)
    seller_description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (self.author.username + " - " + self.event.title)
    class Meta:
       ordering = ['-created_at']