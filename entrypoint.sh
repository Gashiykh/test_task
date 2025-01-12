#!/bin/sh

echo "Waiting for PostgreSQL..."
while ! nc -z postgres 5432; do
  sleep 1
done

echo 

python manage.py migrate

PGPASSWORD=simplepass123 psql -h postgres -U testuser -d testdb -f /app/myproject/data.sql

python manage.py runserver 0.0.0.0:8000
