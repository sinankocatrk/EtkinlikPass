

from django.contrib import admin
from django.urls import path
from . import views






app_name= "api"



urlpatterns = [

    path('register/', views.registerUser, name="register"),
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', views.LogoutView.as_view(), name='user-logout'),

    path('profile/', views.getUserProfile, name="users-profile"),
    path('profile/update', views.updateUserProfile, name="users-profile-update"),
    path('', views.getUsers, name="users"),
    path('<str:pk>/', views.getUserById, name='user'),
    path('update/<str:pk>/', views.updateUser, name='user-update'),
    
    path('advert/', views.AdvertList.as_view(), name='advert-list'),
    path('advert/<int:pk>/', views.AdvertDetail.as_view(), name='advert-detail'),
    path('addadvert/', views.AddAdvertisement.as_view(), name='add-advert'),

]