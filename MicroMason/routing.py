from channels.routing import ProtocolTypeRouter, URLRouter

from channels.auth import AuthMiddlewareStack

import basepage.routing
from basepage.middleware import TokenAuthMiddleware

application = ProtocolTypeRouter({
    # AuthMiddlewareStack
    'websocket': TokenAuthMiddleware(
        URLRouter(basepage.routing.websocket_urlpatterns)
    ),
})