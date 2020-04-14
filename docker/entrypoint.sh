#!/bin/bash

exec gunicorn --bind :8000 main.wsgi:application
