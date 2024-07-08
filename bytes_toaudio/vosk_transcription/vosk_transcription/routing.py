from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path, re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/transcription/$', consumers.TranscriptionConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    'websocket': URLRouter(websocket_urlpatterns),
})


