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
from .serializers import UserLoginSerializer,AdvertSerializer
from user.models import CustomUser
from advert.models import Advert


class UserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return Response({"message": "Başarıyla giriş yaptınız."}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Kullanıcı adı veya parola hatalı."}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'message': "Logout successful"})


def index(request):
    return render(request,"index.html")

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



