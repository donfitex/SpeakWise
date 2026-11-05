# Local development

Use Python 3.12, Node 24, Docker Engine with Compose v2. Copy `.env.example` to `.env`, generate a random Django secret (`python -c 'import secrets; print(secrets.token_urlsafe(48))'`), and set a local PostgreSQL password. Never commit those values. PostgreSQL/Redis ports are private to Compose; API/frontend bind loopback.

Run `docker compose up --build -d`, then `docker compose exec api python backend/manage.py seed_demo` after the curriculum phase. Check `docker compose ps` and request `/api/v1/health/` through port 8000. The frontend is on port 5173. Stop with `docker compose down`; add `--volumes` only to intentionally delete local data. Persistent audio storage is shared by API/worker, never served as static media.

Build-time trust uses a read-only system CA BuildKit secret. In a managed cloud use the platform combined CA at `/etc/ssl/certs/ca-certificates.crt` and retain Docker's proxy configuration. Never disable TLS checks. `SYSTEM_CA_BUNDLE` can select another combined trust bundle on other platforms.

Phase 02 defines the stack; API and frontend entry points arrive in Phases 03–04. Until then a full start is expected to fail. Container startup must be rechecked after those phases.
