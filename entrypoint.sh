#!/bin/bash

# Остановить выполнение при ошибке
set -e

echo "Applying database migrations..."
python manage.py migrate

echo "Starting server..."
exec "$@"