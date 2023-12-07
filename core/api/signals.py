
from django.db.models.signals import pre_save
from .models import CustomUser as User

def updateUser(sender, instance, **kwargs):
    user = instance

    if user.email != '':
        user.username = user.email

pre_save.connect(updateUser, sender=User)