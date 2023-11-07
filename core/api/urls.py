

from django.contrib import admin
from django.urls import path
from . import views

from api.views import UserCreateView,UserLoginView,LogoutView
from api.views import AdvertList,AdvertDetail,AddAdvertisement



app_name= "api"



urlpatterns = [

    path('register/', UserCreateView.as_view(), name='user-create'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', LogoutView.as_view(), name='user-logout'),
    
    path('advert/', AdvertList.as_view(), name='advert-list'),
    path('advert/<int:pk>/', AdvertDetail.as_view(), name='advert-detail'),
    path('addadvert/', AddAdvertisement.as_view(), name='add-advert'),

]