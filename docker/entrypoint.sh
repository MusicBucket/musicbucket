#!/bin/bash

if [[ -z "${RQWORKER}" ]]; then
  echo "Applying database migrations..." &&
    CACHE_TYPE=dummy SECRET_KEY=musicbucket python manage.py migrate

  gunicorn --timeout 120 --bind :8000 main.wsgi:application
else
  SECRET_KEY=musicbucket python manage.py rqworker
fi
