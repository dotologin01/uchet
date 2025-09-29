# 1. Базовый образ с Python
FROM python:3.10-slim

# Установка переменных окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 2. Установка системных зависимостей (Nginx и Supervisor)
RUN apt-get update && apt-get install -y nginx supervisor

# 3. Копирование конфигурационных файлов
COPY ./docker_config/nginx.conf /etc/nginx/sites-available/default
COPY ./docker_config/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# 4. Установка рабочей директории
WORKDIR /app

# 5. Установка зависимостей Python
COPY ./requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 6. Копирование всего проекта в контейнер
COPY . /app/

# 7. Сбор статических файлов
RUN python manage.py collectstatic --no-input

# 8. Запуск Supervisor
CMD ["/usr/bin/supervisord"]