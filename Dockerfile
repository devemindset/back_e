# Étape 1 : build avec toutes les dépendances système
FROM python:3.11.10-slim AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    libffi-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --prefix=/install --no-cache-dir -r requirements.txt

# Étape 2 : image finale minimaliste
FROM python:3.11.10-slim

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copie les packages installés depuis l'étape 1
COPY --from=builder /install /usr/local

# Copie le projet
COPY . .

ENV PYTHONPATH=/usr/src/app/back_down_time_note/back_down_time_note

# Healthcheck optionnel
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "back_down_time_note.wsgi:application"]
