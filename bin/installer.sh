#!/bin/sh

apt-get install pip gunicorn supervisor postgresql libpq-dev
pip install django django-tinymce uvicorn uvloop requests psycopg2