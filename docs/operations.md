# Deployment and operations

## Target and boundaries

Neon PostgreSQL is the selected hosted database; see neon.md. The production Compose stack provides Caddy/static frontend, Gunicorn API, Celery worker, one scheduler, and private Redis. It does not provision a Neon project, host, public domain, SMTP account, private object storage, or backups. No paid resource has been provisioned. A local filesystem private volume is suitable for a single-host demo; use a reviewed private storage backend before multi-host deployment. Verify disk encryption/access controls with the host provider.

## Configure and start

1. Copy `.env.production.example` to ignored `.env.production`. Generate a strong Django secret. Securely set the actual Neon `DATABASE_URL` and verify exact-host PostgreSQL/TCP access plus TLS trust. For web use pooled Neon access; migrations may use the direct endpoint. Never use development learner data in production.
2. Set DOMAIN, DJANGO_ALLOWED_HOSTS, CSRF_TRUSTED_ORIGINS, and a verified sender/SMTP transport. Set public BIND_ADDRESS and standard HTTP_PORT=80 / HTTPS_PORT=443 only on an authorized deployment host. Ensure DNS resolves there. Compose defaults deliberately bind loopback on 8080/8443.
3. Run `docker compose --env-file .env.production -f compose.production.yaml build`. BuildKit mounts a combined CA for package downloads without persisting proxy trust secrets in image layers.
4. Back up the database. Run `docker compose --env-file .env.production -f compose.production.yaml run --rm api python backend/manage.py migrate --noinput`. Migrations must finish before starting workers/API. Create staff accounts with the interactive createsuperuser command; never ship a shared default password. Optionally seed only synthetic demo content with seed_demo.
5. Run `docker compose --env-file .env.production -f compose.production.yaml up -d --wait`. Request `/api/v1/health/` over HTTPS, confirm the static app and a synthetic typed journey, check worker ping, and confirm the scheduler is running. Run `manage.py check --deploy` inside the API container. Do not silence failures merely to launch.

Caddy terminates TLS and keeps the API private. TRUST_PROXY_TLS is enabled only in this isolated production network. Internal API proxy traffic bypasses the outbound Internet proxy for the `api` service only; external traffic retains the environment proxy. No database/Redis/API ports are published. The application never serves private audio as static media. Caddy caps request size and supplies CSP/security headers; API/worker run as a non-root user.

## Backups, restore, and retention

Use Neon branch snapshots/PITR according to your actual plan; verify retention and cost rather than assuming free-tier guarantees. Before migrations, take an encrypted restricted-access backup via your approved database tool. Test restoration into a separate Neon branch, apply migrations, run health and synthetic journey checks, verify ownership and sample record counts, then reapply deletions after the backup timestamp. Never overwrite production to test a restore. Preserve a restricted deletion ledger outside restored data and expire backups per policy (recommended maximum 30 days). Backups/restore are not yet verified in a live Neon project.

Raw audio normally disappears after processing and expires in ten minutes. A single scheduler runs cleanup every five minutes and inactive-session cleanup daily. Alert if it stops. Use `purge_audio` and `purge_learner_data` as documented recovery commands; private-media orphan review is required after storage/database failures. Do not include raw audio in general backups. Keep provider retention separate from your own policy.

## Failure recovery and observability

Health checks query PostgreSQL; worker ping checks Redis/Celery. Monitor HTTP error rate, latency, database connections, queue depth, worker restarts, disk usage, and scheduler heartbeat without logging payloads. Default Gunicorn access logging is disabled; configure redacted log rotation/retention at the host. Treat logs as sensitive. Debug mode must stay off.

To disable speech, set SPEECH_PROVIDER=disabled and recreate API/worker/scheduler; typed lessons remain available. Free offline transcription can be enabled with SPEECH_PROVIDER=pocketsphinx; review its recognition limits first. Optional OpenAI transcription is paid: set provider budget/rate alerts and an account spending cap before enabling it. No pronunciation calibration or release-quality speech score is provided. Redis uses noeviction so memory pressure fails visibly rather than silently dropping jobs; alert and drain/recover deliberately.

For incidents: restrict access, disable affected providers/endpoints, preserve minimal redacted evidence, rotate exposed credentials, assess learner impact, and use a verified private reporting channel. Contact and legal notification obligations must be assigned before launch.

## Current validation

A separate local staging project exercised the production images with isolated local PostgreSQL (not Neon), Gunicorn, Caddy internal TLS, worker, scheduler, and verified CA requests. A copied-source permission issue was fixed for the non-root image user. HTTPS health/static responses passed with certificate verification enabled. The staging in-memory mailer correctly fails Django's deployment check; real SMTP delivery remains a release gate. Public TLS/DNS, live Neon, provider storage/backup restore, cost controls, and production capacity are unverified.
