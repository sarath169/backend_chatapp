from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(
        r'ws/chat/(?P<room_name>\w+)/(?P<uuid>[\w.@+-]+)/$',
        consumers.ChatRoomConsumer.as_asgi()
    ),
    re_path(
        r'^messages/(?P<user_id>\w+)/$',
        consumers.ChatConsumer.as_asgi()
    ),
]