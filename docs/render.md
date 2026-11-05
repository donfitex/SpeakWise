# SpeakWise free Render pilot

One free Docker web service runs Caddy and one Gunicorn process. Accounts,
sessions, lessons, and progress live in the existing Neon PostgreSQL project.
No Render disk, Redis, paid worker, or paid cron is required.

The frontend and API share an HTTPS origin, preserving session/CSRF cookies.
Render's hostname is added automatically to allowed hosts and trusted origins.
Custom domains require explicit DJANGO_ALLOWED_HOSTS and CSRF_TRUSTED_ORIGINS.

## Credentials

- DJANGO_SECRET_KEY: generated privately; the Blueprint can generate it too.
- DATABASE_URL: the existing SpeakWise Neon database URL with TLS verification.
- No AI key or SMTP credentials are required for this pilot.

## Free-tier limits and feature scope

Render can suspend an idle free service. First visits can be slow; availability,
usage quotas, and build limits follow the account's current free allowance.
The filesystem is ephemeral. Never use SQLite for real accounts or progress.
Only one Gunicorn process is supported with the in-memory rate-limit cache.
Rate limits reset on restarts; this configuration is for a small advisory pilot.

Audio uploads are rejected before files or jobs are created. There is no
background transcription. Typed exercises and browser model speech remain
available. Enable audio only after adding private durable storage, a broker,
and reliable background processing.

Password-reset requests return an explicit unavailable response. No reset
tokens or messages are written to logs. To enable email later, configure an
HTTPS email delivery backend supported by the host, verify delivery, and then
enable PASSWORD_RESET_ENABLED. SMTP is not a dependency of the free pilot.

Retention cleanup runs at startup and hourly while the web service is awake.
It cannot run while Render suspends the service, so timed cleanup is best
effort. Do not treat this pilot as satisfying continuous production retention.

## Startup and verification

Startup checks secure settings, applies Django migrations, cleans expired
learner data, and seeds fictional curriculum when SEED_DEMO=true. Set that
variable false after the first deployment. Use a dedicated database, and back
up existing data before migrations.

Verify HTTPS health, registration/login, placement, a typed lesson and saved
progress. Verify unavailable audio and password-reset responses. No shared
administrator password is shipped. The existing educational-review,
speech-calibration, backup/restore, and production-capacity gates remain.
