#!/usr/bin/env bash

python manage.py migrate
daphne --bind 0.0.0.0 --port 8000 config.asgi:application

