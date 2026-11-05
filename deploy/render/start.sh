#!/bin/sh
set -eu
: "${DJANGO_SECRET_KEY:?Set DJANGO_SECRET_KEY}"
: "${DATABASE_URL:?Set DATABASE_URL}"
: "${REDIS_URL:?Set REDIS_URL}"
: "${EMAIL_HOST:?Set EMAIL_HOST}"
: "${EMAIL_HOST_USER:?Set EMAIL_HOST_USER}"
: "${EMAIL_HOST_PASSWORD:?Set EMAIL_HOST_PASSWORD}"
: "${DEFAULT_FROM_EMAIL:?Set DEFAULT_FROM_EMAIL}"
mkdir -p /var/data/private-media
python backend/manage.py check --deploy --fail-level WARNING
python backend/manage.py migrate --noinput
if [ "${SEED_DEMO:-false}" = "true" ]; then
    python backend/manage.py seed_demo
fi
exec /usr/bin/supervisord -c /app/deploy/render/supervisord.conf
