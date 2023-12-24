from django.db import models
from event.models import Event
from user.models import CustomUser as User 
from django.conf import settings

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


class DeleteReason(models.Model):
    REASON_CHOICES = [
        ('sold', 'İlan Satıldı'),
        ('withdraw', 'Satmaktan Vazgeçildi')
    ]

    advert = models.OneToOneField(Advert, on_delete=models.CASCADE)
    reason = models.CharField(max_length=100, choices=REASON_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.advert} - {self.reason}"
    
class ComplaintReason(models.Model):
    REASON_CHOICES = [
        ('overpriced', 'Fiyat piyasasının üzerinde'),
        ('offensive', 'İlan hakaret içeriyor'),
        ('deceptive', 'Aldatıcı ilan'),
        ('other', 'Diğer'),
    ]
    advert = models.ForeignKey(Advert, on_delete=models.CASCADE)
    reason = models.CharField(max_length=100, choices=REASON_CHOICES)
    additional_info = models.TextField(null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.advert} - {self.reason}"