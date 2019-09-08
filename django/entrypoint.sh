#!/usr/bin/env bash

cd webpack
npm install && npm run build
cd ..
python3 manage.py collectstatic --no-input
python3 manage.py makemigrations
python3 manage.py migrate
gunicorn -D -b 0.0.0.0:8000 config.wsgi
