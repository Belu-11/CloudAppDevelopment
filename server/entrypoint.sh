#!/bin/sh
echo "Making migrations and migrating the db."
python manage.py makemigrations
python manage.py migrate