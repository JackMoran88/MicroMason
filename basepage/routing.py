from django.urls import re_path, path

from .consumers import *

websocket_urlpatterns = [
    path("api/ws/notifications/", NotificationConsumer.as_asgi(), name="ws_notifications"),
]

