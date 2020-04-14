#!/bin/bash


echo "Applying database migrations..." && \
    CACHE_TYPE=dummy SECRET_KEY=musicbucket python manage.py migrate

gunicorn --bind :8000 main.wsgi:application
