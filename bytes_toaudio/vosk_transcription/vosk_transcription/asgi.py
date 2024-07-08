import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import vosk_transcription.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vosk_transcription.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            vosk_transcription.routing.websocket_urlpatterns
        )
    ),
})
