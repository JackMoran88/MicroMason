from django.urls import re_path, path

from .consumers import *

websocket_urlpatterns = [
    path("ws/notifications/", NotificationConsumer, name="ws_notifications",
         ),
]
