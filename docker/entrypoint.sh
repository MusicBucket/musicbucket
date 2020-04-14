#!/bin/sh

mkdir -p /data/static && mkdir -p /data/media && \
    echo "Compiling messages..." && \
    CACHE_TYPE=dummy SECRET_KEY=musicbucket python manage.py compilemessages && \
    echo "Compressing..." && \
    CACHE_TYPE=dummy SECRET_KEY=musicbucket python manage.py compress --traceback --force && \
    echo "Collecting statics..." && \
    CACHE_TYPE=dummy SECRET_KEY=musicbucket python manage.py collectstatic --noinput --traceback -v 0 && \
    chmod -R 777 /data/

gunicorn --bind :8000 main.wsgi:application
