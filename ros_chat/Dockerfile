FROM python:3.12-slim-bullseye AS django-static-builder

# Устанавливаем зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app


COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
RUN ./manage.py collectstatic --noinput

#python manage.py migrate
#python manage.py drf_create_token <username>

CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "ros_chat.asgi:application"]