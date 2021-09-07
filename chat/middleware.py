from django.contrib.auth.models import AnonymousUser

from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND)
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware

@database_sync_to_async
def get_user(token_key):
    try:
        print(token_key, "token_key in get_user")
        token = Token.objects.get(key=token_key)
        print(token, "token in get_user")
        return token.user
    except Token.DoesNotExist:
        return AnonymousUser()

class TokenAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        if scope['query_string']:
            print("indside middleware if condition")
            try:
                print(scope['query_string'], "middleware")
                # token_key = (dict((x.split('=') for x in scope['query_string'].decode().split("&")))).get('token', None)
                token_key = scope['query_string'].decode().split('=')[1]
                print(token_key, "token_key")
            except ValueError:
                token_key = None
            scope['user'] = AnonymousUser() if token_key is None else await get_user(token_key)
            print(scope['user'])
            return await super().__call__(scope, receive, send)
        else:
            print("indside middleware else condition")
            scope['error'] = "check for token in the query string"
            print(scope, "else of querystring")
            return Response(scope)