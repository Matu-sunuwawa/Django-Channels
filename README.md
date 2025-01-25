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















