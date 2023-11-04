from django.urls import path
from . import views

urlpatterns = [
    path('myadvert/', views.myadvert,name= "myadvert"),
    path('addadvert/', views.addadvert,name= "addadvert"),     
]