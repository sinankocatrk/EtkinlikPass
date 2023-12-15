from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from core.consumers import Consumer  # İlgili WebSocket consumer'ınız

websocket_urlpatterns = [
    path('ws/path/', Consumer.as_asgi()),
]

application = ProtocolTypeRouter({
    # Diğer protokoller...
    'websocket': AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
