from django.urls import path
from . import views
app_name = 'advert'

urlpatterns = [
    path('', views.index,name= "index"),
    path('myadvert/', views.myadvert,name= "myadvert"),
    path('addadvert/', views.addadvert,name= "addadvert"),
    path('advertdetail/<int:id>/', views.advertdetail, name='advertdetail'),
    path('update/<int:id>/', views.update,name= "update"),   
    path('delete/<int:id>/', views.delete,name= "delete"),   
]