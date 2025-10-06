# Файл: nginx/Dockerfile

# Базовый образ
FROM nginx:1.21-alpine

# Удаляем стандартную конфигурацию
RUN rm /etc/nginx/conf.d/default.conf

# Копируем нашу конфигурацию
COPY nginx.conf /etc/nginx/conf.d