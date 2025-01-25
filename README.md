# 🚀Django-Channels

## Basic Setup
```
python3 -m venv channelenv
```
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
  In the chat/urls.py file include the following code:
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
  The next step is to point the root URLconf at the chat.urls module. In mysite/urls.py:
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
  This one is really basic ideas behind Django-channels which you need to understand what is going on...

  *Let’s start by creating a `routing configuration` for Channels. A Channels routing configuration is an `ASGI application` that is similar to a `Django URLconf`, 
  in that it `tells Channels what code to run when an HTTP request is received` by the Channels server.
</p>


















