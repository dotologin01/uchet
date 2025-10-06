#!/bin/sh

# Применяем миграции базы данных
echo "Applying database migrations..."
python manage.py migrate --no-input

# Собираем статические файлы
echo "Collecting static files..."
python manage.py collectstatic --no-input

# Запускаем Gunicorn
echo "Starting Gunicorn..."
gunicorn student_tracker.wsgi:application --bind 0.0.0.0:8000