# syntax=docker/dockerfile:1
FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1 \
    OTREE_PRODUCTION=1

WORKDIR /app

# 1) install deps first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2) now copy your oTree project (must include settings.py, apps, etc.)
COPY . .

# 3) expose and run
EXPOSE 8000
CMD ["otree", "prodserver", "8000"]