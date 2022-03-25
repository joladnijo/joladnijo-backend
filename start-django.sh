#!/bin/sh

python manage.py check_db
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
