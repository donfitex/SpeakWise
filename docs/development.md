# Local development

Use Python 3.12, Node 24/npm, Docker Engine, Compose v2, and FFmpeg for host-side audio tests. Run `python scripts/configure_local.py` to create `.env` only if it does not already exist; random local secrets are not printed. Never commit `.env`.

`make dev` builds API/frontend/worker/scheduler, starts PostgreSQL/Redis with health checks, applies migrations, and seeds idempotent fictional lessons. Frontend binds loopback port 5173, API 8000. PostgreSQL and Redis stay private. `docker compose ps` plus the API health request confirms readiness. `docker compose exec -T api python backend/manage.py check_speech_worker` exercises a real disabled-provider job using synthetic WAV audio, then removes it.

`make install` installs exact snapshots into `.venv` and frontend/node_modules. `make check` runs relevant quality gates. Activate `.venv` for individual Python commands. `cd frontend && npm run dev` proxies `/api` to the host API by default; inside Compose API_PROXY_TARGET selects the service. The proxy preserves the original host for Django validation.

For host API development with local PostgreSQL, use your own local database URL; Compose intentionally does not expose its database port. Alternatively run Python commands with `docker compose exec api`. For tests use `pytest -q` with SQLite or TEST_POSTGRES=true only on a dedicated PostgreSQL test-capable branch. Never run tests against production.

For browser tests with the stack running, `cd frontend && CHROMIUM_PATH=/usr/bin/chromium npm run test:e2e`. If using Playwright's installed browser, omit CHROMIUM_PATH. The runner can start host services if absent; configure/migrate the database first. Screenshots/traces contain only synthetic test accounts and stay in ignored test-results unless deliberately selected for documentation.

Stop with `make stop`. Add `--volumes` to compose down only when intentionally deleting local data. Installation dependencies persist; running services must be restarted after a cloud snapshot restore. Use existing isolated checkouts; do not create Git worktrees unless requested.

Build trust uses a read-only combined CA secret. Managed cloud Docker retains its configured proxy; never disable verification. SYSTEM_CA_BUNDLE selects a combined trust bundle on other platforms. Private media is shared only by API/worker/scheduler and never served as static files. See operations.md for production, neon.md for hosted PostgreSQL.
