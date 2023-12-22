from django.contrib import admin
from django.urls import path,include
from advert import views
from user import views
from event import views
from chat import views
from django.conf import settings
from django.conf.urls.static import static
from advert import views
from api import views
from .views import index

app_name = 'core'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index,name= "index"),
    path('user/', include("user.urls")),
    path('event/', include("event.urls")), 
    path('advert/', include("advert.urls")),
    path('api/', include("api.urls")),
    path('chat/', include("chat.urls")),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
