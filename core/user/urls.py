from django.contrib import admin
from django.urls import path
from . import views
from .views import profile
app_name= "user"

urlpatterns = [
    path('register/', views.register,name= "register"),
    path('login/', views.loginUser,name= "login"),
    path('logout/', views.logoutUser,name= "logout"),
    path('profile/<int:id>/', views.profile,name= "profile"),
    path('profile_edit/', views.profile_edit, name='profile_edit'),

]