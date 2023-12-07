
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from user.models import CustomUser
from advert.models import Advert

class UserSerializer(serializers.ModelSerializer):
     
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'is_staff')
        
    def save(self, **kwargs):
        return super().save(**kwargs)
    
    def get__id(self):
       return self.id
    
    def get_isAdmin(self):
        return self.is_staff
    
    def get_name(self):
        return self.username   
    


class UserSerializerWithToken(serializers.ModelSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'token')

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)
    
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ('username', 'password')

class UserLogoutSerializer(serializers.Serializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')
    

class AdvertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advert
        fields = ('event', 'author', 'price', 'seller_description')






