#!/usr/bin/env bash

cd chattr
python manage.py migrate
python manage.py loaddata chat/fixtures/channels.json
python manage.py runserver 0.0.0.0:8000
