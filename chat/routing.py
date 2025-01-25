# chat/routing.py
from django.urls import re_path

from . import consumers

# ws://127.0.0.1:8000/ws/chat/lobby/ ... /ws/chat/(?P<room_name>\w+)/$
websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
]