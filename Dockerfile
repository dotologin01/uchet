# Файл: Dockerfile

# Базовый образ
FROM python:3.10-slim

# Переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Рабочая директория
WORKDIR /app

# Установка зависимостей
COPY ./requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копирование проекта
COPY . /app/

# Копирование и предоставление прав на запуск entrypoint скрипту
COPY ./entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh