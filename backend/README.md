# Backend

Django/DRF modular monolith. `config` holds settings/URLs/Celery; `accounts`, `curriculum`, `placement`, `classroom`, `speech`, `assessment`, and `progress` own their models and behavior. `core` provides health, OpenAPI contracts, request parsing, and operational commands. Staff content controls use Django admin.

From the repository root use the locked development dependencies, `.env` configuration, and `python backend/manage.py <command>`. Compose applies PostgreSQL migrations on local startup. Tests use SQLite by default; TEST_POSTGRES=true uses the configured PostgreSQL database and creates a separate test database. Never point that mode at a production branch. See root README and docs/operations.md.
