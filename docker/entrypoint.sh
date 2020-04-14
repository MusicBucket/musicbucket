#!/bin/sh



gunicorn --bind :8000 main.wsgi:application
