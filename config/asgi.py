import os

from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing
import notifications.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

django_asgi_app = get_asgi_application()


from config.ws_middleware import TokenAuthMiddleware

application = ProtocolTypeRouter({
    # HTTP so'rovlari — oddiy Django
    "http": django_asgi_app,
    # WebSocket so'rovlari — Channels (JWT token orqali auth)
    "websocket": TokenAuthMiddleware(
        URLRouter(
            chat.routing.websocket_urlpatterns
            + notifications.routing.websocket_urlpatterns
        )
    ),
})