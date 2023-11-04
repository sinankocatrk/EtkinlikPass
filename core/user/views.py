from django.shortcuts import render,redirect
from .forms import LoginForm 
from django.contrib.auth.models import User 
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserLoginSerializer
from .forms import CustomUserCreationForm 





def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Başka işlemler yapabilirsiniz
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def loginUser(request):
    form = LoginForm(request.POST or None)
    context = {
            "form" : form
        }

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(username = username,password = password)

        if user is None:
            messages.info(request,"Kullanıcı Adı veya Parola Hatalı")
            return render(request,"login.html",context)

        messages.success(request,"Başarıyla Giriş Yaptınız")

        login(request,user)
        return redirect("index")
    return render(request,"login.html",context)


def logoutUser(request):
    logout(request)
    messages.success(request,"Başarıyla çıkış yaptınız.")
    return redirect("index")

def index(request):
    return render(request,"index.html")