from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name= "index"),
    path('myadvert/', views.myadvert,name= "myadvert"),
    path('addadvert/', views.addadvert,name= "addadvert"),
    path('advertdetail/<int:id>', views.advertdetail,name= "advertdetail"),
]