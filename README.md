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





















