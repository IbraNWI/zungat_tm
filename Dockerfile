FROM python:3.12-slim

# Установка переменных окружения
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Рабочая директория внутри контейнера
WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Копирование проекта
COPY . .

# Создаем папку для статики (если нет)
RUN mkdir -p staticfiles

# Сбор статики (выполнится при сборке, но лучше при запуске)
# CMD будет переопределен в docker-compose, но команда нужна
# RUN python manage.py collectstatic --noinput

# Запуск через Gunicorn
# --workers 1 критично для SQLite!
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "1", "zungat_tm.wsgi:application"]