#!/bin/sh

python3 manage.py makemigrations common
python3 manage.py makemigrations users
python3 manage.py makemigrations tasks
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:8000
