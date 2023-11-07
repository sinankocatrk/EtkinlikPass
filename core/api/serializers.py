
from rest_framework import serializers

from user.models import CustomUser
from advert.models import Advert

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password')


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ('username', 'password')

class UserLogoutSerializer(serializers.Serializer):
    class Meta:
        model = CustomUser
        fields = ()

class AdvertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advert
        fields = ('event', 'author', 'price', 'seller_description')






