# Neon PostgreSQL

Neon is the selected hosted database. Use a dedicated development branch, never production learner data for local tests. In Neon, copy the PostgreSQL connection string and set `DATABASE_URL` securely in the runtime environment or ignored `.env`. Do not paste passwords in issues/chat or put them in frontend variables. No Neon credentials or live database are configured by this repository.

Connections to `*.neon.tech` enforce `sslmode=verify-full` and short-lived connections. Use the pooled hostname for the web API; for migrations use the direct hostname through a command-scoped `DATABASE_URL` if needed. Both use the same schema. Preserve CA verification. Ordinary libpq TCP access must be permitted to the exact Neon host on 5432 by your execution environment; an HTTPS secret placeholder is not a raw PostgreSQL password. An HTTP allowlist alone does not establish PostgreSQL connectivity.

After securely setting the URL, run `python backend/manage.py check --database default`, `python backend/manage.py migrate --noinput`, and request `/api/v1/health/`. Back up the branch before destructive migrations. Free-tier limits, suspension, and retention vary; verify your plan before pilot deployment. Local Compose PostgreSQL remains the offline/CI fallback.
