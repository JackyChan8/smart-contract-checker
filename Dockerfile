# Используем официальный Python образ как базовый
FROM python:3.13-slim

# Установка зависимостей системы
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории внутри контейнера
WORKDIR /opt/app

# Копируем файлы зависимостей
COPY requirements.txt /tmp/requirements.txt

# Установка Python-зависимостей
RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt

# Копируем всё приложение в рабочую директорию контейнера
COPY . .

# Команда по умолчанию для запуска uvicorn в режиме разработки
CMD ["python", "main.py"]