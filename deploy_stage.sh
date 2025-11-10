#!/bin/bash

# Прекращаем выполнение скрипта, если любая команда завершится с ошибкой
set -e

# Переходим в директорию проекта на сервере
# Укажите ваш реальный путь
PROJECT_DIR="/opt/student-tracker"
cd $PROJECT_DIR

# 1. Обновляем код из Git, чтобы docker-compose.yml был актуальным
echo "Pulling latest code from develop branch..."
git checkout develop
git pull origin develop

# 2. Логинимся в Docker Hub, чтобы иметь возможность скачивать образы
# Переменные DOCKER_USER и DOCKER_PASSWORD должны быть заданы в TeamCity
echo "Logging in to Docker Hub..."
echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USER" --password-stdin

# 3. Скачиваем свежие образы, указанные в docker-compose.yml
echo "Pulling latest images..."
docker-compose pull

# 4. Перезапускаем сервисы.
# --force-recreate заставит пересоздать контейнеры, даже если их конфигурация не изменилась, но образ обновился.
# -d для запуска в фоновом режиме.
echo "Restarting services..."
docker-compose up -d --force-recreate

# 5. (Опционально) Очищаем систему от старых, неиспользуемых образов
echo "Cleaning up old images..."
docker image prune -f

echo "Deployment finished successfully!"