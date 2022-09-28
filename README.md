# chattr-backend

Chattr is a very simple chat service based on websockets.

It supports multiple channels and saving the messages to a database.

Every channel has its own websocket, and the messages are sent as json as follows:

```json
{
  "username": "pertsa",
  "message": "Hello, I just joined the channel!",
  "timestamp": "2022-09-28 19:50:54.537565+00:00"
}
```

There is a basic testing chat interface served by the backend as well at `http://<server>/chat/`. It also serves the channel list as json at `http://<server>/chat/list/`.

## Usage

### Development

```sh
# install dependencies
$ python3 -m venv venv
$ . venv/bin/activate
(venv) $ pip3 install -r requirements.txt

# set up the database and initial data
(venv) $ cd chattr
(venv) $ python3 manage.py migrate
(venv) $ python3 manage.py loaddata chat/fixtures/channels.json

# create a superuser (optional)
(venv) $ python3 manage.py createsuperuser

# running
(venv) $ python3 manage.py runserver
```

### Production or something

Install Docker, then

```sh
$ docker build -t chattr:1 .
$ docker run -p 8000:8000 chattr:1
```

Don't forget to disable the debug mode and change the secrets. You may need to set some allowed hosts as well. Imagine if there were environment variables for that.
