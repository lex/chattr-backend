# chattr-backend

## Usage

### Development

```sh
# install dependencies
$ python3 -m venv venv
$ . venv/bin/activate
(venv) $ pip3 install -r requirements.txt

# set up the database and initia ldata
(venv) $ cd chattr
(venv) $ python3 manage.py migrate
(venv) $ python3 manage.py loaddata chat/fixtures/channels.json

# create a superuser (optional)
(venv) $ python3 manage.py createsuperuser

# running
(venv) $ python3 manage.py runserver
```
