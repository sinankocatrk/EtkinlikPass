from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True) 
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    city = models.CharField(max_length=30, blank=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    password = models.CharField(max_length=30, blank=False )
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    favorites = models.ManyToManyField('advert.Advert', related_name='favorited_by', blank=True)

class UserRelation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

