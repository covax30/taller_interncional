#!/bin/bash

# exit on error
set -e

# Wait for MySQL to be ready
echo "Waiting for database..."
while ! python manage.py shell -c "import django; django.setup(); from django.db import connections; connections['default'].ensure_connection()" > /dev/null 2>&1; do
  sleep 1
done
echo "Database ready!"

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput
python manage.py migrate --database=log_db --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start the application
echo "Starting application..."
exec "$@"
