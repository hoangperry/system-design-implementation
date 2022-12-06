#!/bin/bash

echo "Collect static files"
python3 manage.py collectstatic --noinput
echo "Apply database migrations"
python3 manage.py migrate
python3 manage.py runserver --noreload 0.0.0.0:8000
