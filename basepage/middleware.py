from channels.auth import AuthMiddlewareStack
# from rest_framework.authtoken.models import TokenProxy
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections


class TokenAuthMiddleware:
    """Token authorization"""

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope, receive, send):
        # headers = dict(scope['headers'])
        # if b'authorization' in headers:
        #     try:
        #         token_name, token_key = headers[b'authorization'].decode().split()
        #         if token_name == 'Token':
        #             token = TokenProxy.objects.get(key=token_key)
        #             scope['user'] = token.user
        #             close_old_connections()
        #     except TokenProxy.DoesNotExist:
        scope['user'] = AnonymousUser()
        return self.inner(scope, receive, send)
