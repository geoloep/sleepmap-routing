#!/bin/sh
cd sleepmap

export DJANGO_DEBUG=false

# python3 manage.py migrate
gunicorn sleepmap.wsgi -b 0.0.0.0:8000