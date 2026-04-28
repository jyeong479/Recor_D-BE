FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libpq-dev \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    libffi-dev \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements/ requirements/
RUN pip install --no-cache-dir -r requirements/production.txt

COPY . .

ENV DJANGO_SETTINGS_MODULE=config.settings.production
RUN SECRET_KEY=build-only python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]
