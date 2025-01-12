#!/bin/sh

echo "Waiting for PostgreSQL..."
while ! nc -z postgres 5432; do
  sleep 1
done

echo 

python manage.py migrate


python manage.py runserver 0.0.0.0:8000
