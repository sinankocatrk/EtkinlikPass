from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.chat_index, name='chat_index'),
    path('<int:advert_id>/<int:user_id>/', views.chat_room, name='chat_room'),
]
