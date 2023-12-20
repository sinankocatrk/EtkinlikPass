from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chat.consumers import Consumer  # İlgili WebSocket consumer'ınız

websocket_urlpatterns = [
    path('ws/chat/<int:advert_id>/<int:user_id>/', Consumer.as_asgi()),
]

application = ProtocolTypeRouter({
    # Diğer protokoller...
    'websocket': AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
