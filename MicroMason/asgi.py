"""
ASGI config for MicroMason project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

# import os
#
# from django.core.asgi import get_asgi_application
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MicroMason.settings')
#
# application = get_asgi_application()

import os

from django.conf.urls import url
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MicroMason.settings")
django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import basepage.routing
from basepage.middleware import TokenAuthMiddleware

application = ProtocolTypeRouter({
    # Django's ASGI application to handle traditional HTTP requests
    "http": django_asgi_app,

    # WebSocket chat handler
    'websocket': AuthMiddlewareStack(
        URLRouter(basepage.routing.websocket_urlpatterns)
    ),
})
