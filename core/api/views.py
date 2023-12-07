from django.shortcuts import render,redirect
from user import forms
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserLoginSerializer,AdvertSerializer,UserSerializerWithToken,UserLogoutSerializer
from user.models import CustomUser
from advert.models import Advert
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated, IsAdminUser

@api_view(['POST'])
def registerUser(request):
    data = request.data
    try:
        user = CustomUser.objects.create(
            username=data['username'],
            email=data['email'],
        )
        user.set_password(data['password'])
        user.save()

        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'User with this email already exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializerWithToken(self.user).data

        # Şifreyi hash'le
        hashed_password = make_password(self.user.password)

        # Daha sonra, gerekirse hashed_password'ü kullanabilirsiniz

        for k, v in serializer.items():
            data[k] = v

        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer




class LogoutView(APIView):
    serializer_class = UserLogoutSerializer

    def post(self, request):
        # Kullanıcı bilgilerini al
        user = CustomUser.objects.get(username=request.data['username'])

        # Çıkış yap


        # user değişkenini kullanarak istediğiniz işlemleri yapabilirsiniz
        if user.is_authenticated:
            logout(request)
            
            user.save()
            message = {user.username + ' isimli kullanıcı başarıyla çıkış yaptı.'}
            return Response(message, status=status.HTTP_200_OK)
        elif  not user:
            message = {'detail': 'Böyle bir kullanıcı yok.'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        


def index(request):
    return render(request,"index.html")

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    users = CustomUser.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUserById(request, pk):
    user = CustomUser.objects.get(id=pk)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    user = request.user
    serializer = UserSerializerWithToken(user, many=False)

    data = request.data

    user.first_name = data['name']
    user.username = data['username']
    user.email = data['email']
    if data['password'] != '':
        user.password = make_password(data['password'])
    
    user.save()

    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateUser(request, pk):
    user = User.objects.get(id=pk)

    data = request.data

    user.first_name = data['name']
    user.username = data['email']
    user.email = data['email']


    user.save()

    serializer = UserSerializer(user, many=False)

    return Response(serializer.data)



class AdvertList(generics.ListCreateAPIView):
    queryset = Advert.objects.all()
    serializer_class = AdvertSerializer

class AdvertDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Advert.objects.all()
    serializer_class = AdvertSerializer

class AddAdvertisement(APIView):
    def post(self, request):
        serializer = AdvertSerializer(data=request.data)

        if serializer.is_valid():
            event = serializer.validated_data['event']
            author = serializer.validated_data['author']
            price = serializer.validated_data['price']
            seller_description = serializer.validated_data['seller_description']

            advert = Advert.objects.create(event=event, author=author, price=price, seller_description=seller_description)
            advert.save()

            return Response({"message": "İlan başarıyla oluşturuldu."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



