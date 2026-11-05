FROM node:24-bookworm-slim AS frontend
WORKDIR /build
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

FROM caddy:2 AS caddy
FROM python:3.12-slim-bookworm
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 DJANGO_SETTINGS_MODULE=config.settings.render
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg supervisor ca-certificates && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.lock ./
RUN pip install --no-cache-dir -r requirements.lock
COPY --from=caddy /usr/bin/caddy /usr/bin/caddy
RUN useradd --create-home app && mkdir -p /var/data/private-media /app/backend/staticfiles && chown -R app:app /app /var/data
COPY --chown=app:app backend/ ./backend/
COPY --from=frontend --chown=app:app /build/dist /srv
COPY deploy/render/ /app/deploy/render/
RUN DJANGO_SECRET_KEY=build-only-not-for-runtime DATABASE_URL=sqlite:///:memory: python backend/manage.py collectstatic --noinput
USER app
EXPOSE 10000
CMD ["sh", "/app/deploy/render/start.sh"]
