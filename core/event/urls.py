from django.urls import path
from . import views

urlpatterns = [
    path('fetch-events/', views.fetch_and_save_events, name='fetch_and_save_events'),
]
