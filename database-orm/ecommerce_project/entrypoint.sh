#!/bin/bash

# Exit on error
set -e

echo "Waiting for PostgreSQL to be ready..."
while ! pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done

echo "PostgreSQL is ready!"

# Run migrations
echo "Running database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec "$@"
