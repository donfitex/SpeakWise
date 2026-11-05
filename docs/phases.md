# Delivery record

## Phase 01 — Product and repository foundation

Scope: product/audience boundaries, architecture ADR, contribution and security guidance, safe environment template, editor conventions, generated-file exclusions, backend directory, and preserved master plan.

Validation: dependency consistency and Python imports passed during onboarding. Frontend build remains blocked by missing tsconfig.json; pytest collected no tests. This documentation phase does not claim a runnable application. Phase verification checks whitespace, required files, safe environment placeholders, generated-file exclusion, and tracked changes.

Acceptance: clean-checkout documentation describes scope, current dependency setup, synthetic-data policy, planned architecture, and known limits. No real learner data or secret values added.

Commit: `chore(scaffold): initialize speakwise project`.

Next: Phase 02, local Docker Compose services. Service startup acceptance depends on the Django and frontend entry points introduced by Phases 03 and 04; record that dependency explicitly rather than claiming the full stack starts prematurely.

## Phase 02 — Local developer environment

Added Compose services, health checks, persistent private volumes, Dockerfiles with verified TLS trust, loopback port bindings, and startup documentation. `docker compose config --quiet` validates the configuration. Full application startup depends on Phases 03–04; the full-stack acceptance gate remains pending until then.

## Phase 03 — Backend foundation

Added Django settings split, session-authenticated DRF defaults, versioned API, database-backed health endpoint, OpenAPI route, Celery wiring, production security defaults, and database test configuration. `manage.py check --settings=config.settings.test` and the health API database test pass. PostgreSQL migrations and stack startup will be checked with Compose after frontend entry points exist.

## Phase 04 — Frontend foundation

Added strict TypeScript/Vite entry points, responsive design tokens, semantic navigation, skip link, route fallbacks, and a CSRF-aware API client with offline/error handling. `npm run build` passes. Account/classroom/progress routes are explicitly labelled placeholders for subsequent phases. Browser layout validation is deferred to journey testing.

## Phase 05 — CI and code quality

Added exact Python dependency snapshot, npm lockfile, compatible TypeScript 5.9 (TypeScript 7 was outside the linter peer range), Ruff, ESLint/Prettier, CI on pushes/PRs, migration checks, and review template. Local frontend lint/typecheck/build and backend tests are gates; hosted GitHub Actions execution is not claimed. Docker builds passed and Compose reports all five services healthy after Phases 03–04. Browser HTTP and worker behavior are validated in subsequent integration checks.

## Phase 06 — Accounts and learner profile

Implemented session registration/login/logout, CSRF-protected unauthenticated writes, password reset tokens with non-enumerating responses, owner-only profile/preferences, adult/older-teen pilot eligibility, and append-only audio consent history. Added account UI with reset and preference forms. Three backend tests pass, including cross-user isolation, CSRF rejection, validation, and single-use reset; frontend lint/build pass. Reset email is in-memory locally; a production email transport remains an operator requirement. Neon URL support enforces full TLS verification; live Neon validation awaits secure DATABASE_URL and host access.
