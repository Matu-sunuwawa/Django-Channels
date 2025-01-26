# 🚀Django-Channels

## Basic Setup
```
python3 -m venv channelenv
```
```
pip install daphne==4.1.2
pip install channels=4.0.0
```
Remember: written for `Channels 4.0`, which supports `Python 3.7+` and `Django 3.2+`.
```
django-admin startproject mysite
```
<p>Make sure you’re in the same directory as manage.py and type this command:</p>

```
python3 manage.py startapp chat
```
<p>For this purposes, we will only be working with chat/views.py and chat/__init__.py. So remove all other files from the `chat` directory.</p>

<p>Edit the mysite/settings.py file and add 'chat' to the <mark>INSTALLED_APPS</mark> setting</p>

### Add the index view
<p>
  within `chat` create a file called index.html
  Put the following code in chat/templates/chat/index.html:
</p>

```
<!-- chat/templates/chat/index.html -->
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8"/>
    <title>Chat Rooms</title>
</head>
<body>
    What chat room would you like to enter?<br>
    <input id="room-name-input" type="text" size="100"><br>
    <input id="room-name-submit" type="button" value="Enter">

    <script>
        document.querySelector('#room-name-input').focus();
        document.querySelector('#room-name-input').onkeyup = function(e) {
            if (e.key === 'Enter') {  // enter, return
                document.querySelector('#room-name-submit').click();
            }
        };

        document.querySelector('#room-name-submit').onclick = function(e) {
            var roomName = document.querySelector('#room-name-input').value;
            window.location.pathname = '/chat/' + roomName + '/';
        };
    </script>
</body>
</html>
```

<p>
  Put the following code in chat/views.py:
</p>

```
# chat/views.py
from django.shortcuts import render


def index(request):
    return render(request, "chat/index.html")
```
<p>
  To call the view, we need to map it to a URL - and for this we need a URLconf.
  create a file called `urls.py` in chat directory.
  
  Put the following code in chat/urls.py:
</p>

```
# chat/urls.py
from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
]
```
<p>
  Put the following code in mysite/urls.py:
</p>

```
# mysite/urls.py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("chat/", include("chat.urls")),
    path("admin/", admin.site.urls),
]
```
### Lets Verify:
```
python3 manage.py runserver
```
### Go to <code>http://127.0.0.1:8000/chat/</code>
### Type in “lobby” ... <code>http://127.0.0.1:8000/chat/lobby/</code>
<p>
  Output:
  we haven’t written the room view yet, so you’ll get a <mark>“Page not found”</mark> error page.
</p>

### Prepare for next step ... press Control-C

## Integrate the Channels library
<p>
  So far we’ve just created a regular Django app; we haven’t used the Channels library at all. Now it’s time to integrate Channels.
  Understanding the basic concepts behind Django Channels is crucial to grasp what’s happening under the hood....

  *Let’s start by creating a `routing configuration` for Channels. A Channels routing configuration is an `ASGI application` that is similar to a `Django URLconf`, 
  in that it `tells Channels what code to run when an HTTP request is received` by the Channels server.

  Put the following code in mysite/asgi.py:
</p>

```
# mysite/asgi.py
import os

from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        # Just HTTP for now. (We can add other protocols later.)
    }
)
```
<p>Edit the mysite/settings.py file and add 'daphne' to the top of the INSTALLED_APPS:</p>

```
# mysite/settings.py
INSTALLED_APPS = [
    'daphne',
    'chat',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```
You’ll also need to point `Daphne` at the root routing configuration. Edit the `mysite/settings.py` at bottom of it:
```
# mysite/settings.py
# Daphne
ASGI_APPLICATION = "mysite.asgi.application"
```
*With Daphne now in the `installed apps`, it `will take control of the runserver command`, replacing the `standard Django development server` with the `ASGI compatible version`.
```
python3 manage.py runserver
```
### Output:
*Notice the line beginning with `Starting ASGI/Daphne...`
### Go to <code>http://127.0.0.1:8000/chat/](http://127.0.0.1:8000/chat/</code>
### Prepare for next step ... press Control-C

##Implement a Chat Server
###Add the room view
Create the view template for the room view in `chat/templates/chat/room.html`:
```
<!-- chat/templates/chat/room.html -->
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8"/>
    <title>Chat Room</title>
</head>
<body>
    <textarea id="chat-log" cols="100" rows="20"></textarea><br>
    <input id="chat-message-input" type="text" size="100"><br>
    <input id="chat-message-submit" type="button" value="Send">
    {{ room_name|json_script:"room-name" }}
    <script>
        const roomName = JSON.parse(document.getElementById('room-name').textContent);

        const chatSocket = new WebSocket(
            'ws://'
            + window.location.host
            + '/ws/chat/'
            + roomName
            + '/'
        );

        chatSocket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            document.querySelector('#chat-log').value += (data.message + '\n');
        };

        chatSocket.onclose = function(e) {
            console.error('Chat socket closed unexpectedly');
        };

        document.querySelector('#chat-message-input').focus();
        document.querySelector('#chat-message-input').onkeyup = function(e) {
            if (e.key === 'Enter') {  // enter, return
                document.querySelector('#chat-message-submit').click();
            }
        };

        document.querySelector('#chat-message-submit').onclick = function(e) {
            const messageInputDom = document.querySelector('#chat-message-input');
            const message = messageInputDom.value;
            chatSocket.send(JSON.stringify({
                'message': message
            }));
            messageInputDom.value = '';
        };
    </script>
</body>
</html>
```
Create the view function for the room view in `chat/views.py`:
```
# chat/views.py
from django.shortcuts import render


def index(request):
    return render(request, "chat/index.html")


def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})
```
Create the route for the room view in `chat/urls.py`:
```
# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:room_name>/", views.room, name="room"),
]
```
```
python3 manage.py runserver
```
### Go to `http://127.0.0.1:8000/chat/`
### Type in “lobby” as the room name and press enter and output: http://127.0.0.1:8000/chat/lobby/
Question: Type the message “hello” and press enter. `Nothing happens`. Why?
Answer: The room view is trying to open a WebSocket to the URL ws://127.0.0.1:8000/ws/chat/lobby/ but `we haven’t created a consumer` that accepts WebSocket connections yet.
browser’s JavaScript console:
```
WebSocket connection to 'ws://127.0.0.1:8000/ws/chat/lobby/' failed: Unexpected response code: 500
```
### Write your first consumer
`Important Note(what is going on consumer?):`
When Django accepts an `HTTP request`, it consults the `root URLconf to lookup a view function`, and `then calls the view function` to handle the request. 
`Similarly`, when Channels accepts a `WebSocket connection`, it consults the `root routing configuration` to lookup a consumer, 
and `then calls various functions` on the consumer to handle events from the connection.

`Note That(who the hell are you /ws/):`
It is good practice to use a common path prefix like `/ws/` to distinguish WebSocket connections from ordinary `HTTP connections`

Put the following code in `chat/consumers.py`:
```
# chat/consumers.py
import json

from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        self.send(text_data=json.dumps({"message": message}))
```
This is a `synchronous WebSocket consumer` that accepts all connections, receives messages from its client, 
and echos those messages back to the same client. For now `it does not broadcast messages to other clients in the same room`.
==> so we will rewrite chat server as `Asynchronous`: inorder to enable to broadcast messages to other clients in the same room.

Put the following code in `chat/routing.py` which has a `route to the consumer`:
```
# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
]
```
Put the following code in `mysite/asgi.py`
```
# mysite/asgi.py
import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

from chat.routing import websocket_urlpatterns

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
        ),
    }
)
```
the `ProtocolTypeRouter` will first inspect the `type of connection`. If it is a WebSocket connection (ws:// or wss://), the connection will be given to the `AuthMiddlewareStack`.
The `AuthMiddlewareStack` will populate the connection’s scope with a reference to the currently authenticated user.
### RUN:
```
python manage.py migrate
```
```
python3 manage.py runserver
```
### Go to the room page at `http://127.0.0.1:8000/chat/lobby/`
### Type the message “hello” and press enter. You should now see “hello” echoed in the chat log.
However if you <mark>open a second browser tab</mark> to the same room page at `http://127.0.0.1:8000/chat/lobby/` and type in a message, 
the <mark>message will not appear</mark> in the first tab. For that to work, <mark>we need to have multiple instances of the same ChatConsumer</mark>
be able to talk to each other. Channels provides a `channel laye`r abstraction that enables this kind of communication between consumers.

### Enable a channel layer
A channel layer provides:
*A channel is a mailbox where messages can be sent to
*A group is a group of related channels.

We will use a channel layer that uses `Redis as its backing store`.
```
docker run --rm -p 6379:6379 redis:7
```
If docker is not working fine:
```
systemctl start docker
docker ps
```
```
python3 -m pip install channels_redis
```
*so that Channels knows how to interface with Redis

Edit the `mysite/settings.py`:
```
# mysite/settings.py
# Channels
ASGI_APPLICATION = "mysite.asgi.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}
```
Let’s make sure that the channel layer can communicate with Redis. `Open a Django shell` and <mark>run the following commands</mark>:
```
$ python3 manage.py shell
import channels.layers
channel_layer = channels.layers.get_channel_layer()
from asgiref.sync import async_to_sync
async_to_sync(channel_layer.send)('test_channel', {'type': 'hello'})
async_to_sync(channel_layer.receive)('test_channel')

output(result):{'type': 'hello'}
```
`chat/consumers.py`, replacing the old code:
```
# chat/consumers.py
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))
```
async_to_sync(...) because `ChatConsumer is a synchronous WebsocketConsumer` but it is `calling an asynchronous channel layer` method.(All `channel layer` methods are `asynchronous`.)
```
python3 manage.py runserver
```
Open a `browser tab` to the room page at http://127.0.0.1:8000/chat/lobby/. Open a `second browser tab` to the same room page.
In the second browser tab, type the message “hello” and press enter. You should now see “hello” echoed in the chat log in both 
the <mark>second browser</mark> tab and in the <mark>first browser</mark> tab.

<h3>I Gotcha You My Bro ... Congrats ... You now have a basic <mark>fully-functional</mark> chat server!<h3>

## Rewrite Chat Server as Asynchronous
### Rewrite the consumer to be asynchronous
Put the following code in `chat/consumers.py`:
```
# chat/consumers.py
import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))
```
`new code` is very similar to the `original code`, with the following <mark>differences</mark>:
* ChatConsumer now inherits from `AsyncWebsocketConsumer` rather than `WebsocketConsumer`.
* All methods are `async def` rather than just `def`.
* `await` is used to call asynchronous functions that perform I/O.
* async_to_sync is no longer needed.

```
python3 manage.py runserver
```
### Final Test:
Open a browser tab to the room page at `http://127.0.0.1:8000/chat/lobby/`. Open a second browser tab to the same room page.
In the second browser tab, type the message “hello” and press enter. You should now see “hello” echoed in the chat log in both 
the second browser tab and in the first browser tab.

<h3>🎉Congrats ... Now your chat server is fully asynchronous!</h3>
























