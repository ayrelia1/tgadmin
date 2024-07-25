FROM python:3.9-slim

# Установка необходимых системных пакетов
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    postgresql \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# Установка зависимостей Python
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Копирование файлов приложения
COPY . /app
WORKDIR /app

EXPOSE 80

# Копирование конфигурации Nginx
COPY nginx/nginx.conf /etc/nginx/nginx.conf

# Запуск Nginx и вашего приложения
CMD service nginx start && tail -f /dev/null