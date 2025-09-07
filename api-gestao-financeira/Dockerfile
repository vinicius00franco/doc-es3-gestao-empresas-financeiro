FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM base AS dev
WORKDIR /app
COPY . .
RUN mkdir -p media staticfiles logs && adduser --disabled-password --gecos '' django \
    && chown -R django:django /app
USER django
EXPOSE 8000
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "core.asgi:application"]