# syntax=docker/dockerfile:1
FROM python:3.12-slim-bookworm
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.lock ./
RUN --mount=type=secret,id=system_ca,required=true PIP_CERT=/run/secrets/system_ca pip install --no-cache-dir -r requirements.lock
COPY backend ./backend
RUN useradd --create-home app && mkdir /app/private-media && chown app:app /app/private-media
USER app
CMD ["gunicorn", "--chdir", "backend", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]
