#!/bin/sh
alias python=python3
python manage.py migrate
python manage.py collectstatic --noinput

#python manage.py runserver 0.0.0.0:8000
gunicorn core.wsgi --bind 0.0.0.0:8000