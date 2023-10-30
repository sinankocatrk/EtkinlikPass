from django.contrib import admin
from django.urls import path
from . import views
from .views import UserCreateView
app_name= "user"



urlpatterns = [
    path('register/', views.register,name= "register"),
    path('login/', views.loginUser,name= "login"),
    path('logout/', views.logoutUser,name= "logout"),
    path('api/register/', UserCreateView.as_view(), name='user-create'),
]