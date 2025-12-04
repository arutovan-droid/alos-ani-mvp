# ALOS Customs Broker Dockerfile

FROM python:3.11-slim

# Системные зависимости для torch / sentence-transformers
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Рабочая директория внутри контейнера
WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходники проекта
COPY alos_core/ /app/alos_core/

# Открываем порт сервиса
EXPOSE 8000

# Запускаем FastAPI-приложение
CMD ["uvicorn", "alos_core.customs.api:app", "--host", "0.0.0.0", "--port", "8000"]
