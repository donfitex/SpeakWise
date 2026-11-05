#!/bin/sh
set -eu
: "${DJANGO_SECRET_KEY:?Set DJANGO_SECRET_KEY}"
: "${DATABASE_URL:?Set DATABASE_URL}"
python backend/manage.py check --deploy --fail-level WARNING
python backend/manage.py migrate --noinput
python backend/manage.py purge_learner_data
if [ "${SEED_DEMO:-false}" = "true" ]; then
    python backend/manage.py seed_demo
fi
exec /usr/bin/supervisord -c /app/deploy/render/supervisord.conf
