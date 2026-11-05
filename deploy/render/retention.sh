#!/bin/sh
# Free services sleep when idle. Cleanup also runs synchronously on every startup.
set -eu
while true; do
    python /app/backend/manage.py purge_learner_data
    sleep 3600
done
