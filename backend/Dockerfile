# syntax=docker/dockerfile:1
FROM python:3.12-slim-bookworm
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
RUN --mount=type=secret,id=system_ca,required=true apt-get -o Acquire::https::CaInfo=/run/secrets/system_ca update && apt-get -o Acquire::https::CaInfo=/run/secrets/system_ca install -y --no-install-recommends ffmpeg && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.lock ./
RUN --mount=type=secret,id=system_ca,required=true PIP_CERT=/run/secrets/system_ca pip install --no-cache-dir -r requirements.lock
RUN useradd --create-home app && mkdir /app/private-media && chown app:app /app/private-media
COPY --chown=app:app backend ./backend
RUN DJANGO_SECRET_KEY=build-only-not-a-runtime-secret DATABASE_URL=sqlite:///:memory: python backend/manage.py collectstatic --noinput
USER app
CMD ["gunicorn", "--chdir", "backend", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]
