# Validation evidence

Validated in the managed cloud environment on 2026-11-05. Synthetic sample content and fictional accounts only.

- Backend: 28 pytest tests pass with both SQLite and actual PostgreSQL. Covers auth/CSRF, owner isolation, validation, prerequisite/order/idempotency, content version/reviewer controls, evidence bounds, recommendations, audio decode/failure/expiry/deletion, and retention.
- Frontend: four Vitest behavior tests pass for unsupported recording, consent/permission failure, recording preview/track cleanup, and online model-voice permission.
- Browser: two Chromium/Playwright tests pass: complete signup/preferences/placement/retry/resume/completion/progress/logout journey, plus keyboard skip link. axe checks on landing and desktop/mobile dashboard report no WCAG A/AA violations in those tested states. This is not a full manual screen-reader audit.
- Containers: six Compose services built and started; PostgreSQL migrations, API/frontend HTTP, worker ping, and a real Redis/Celery disabled-provider speech job passed. Audio was removed after processing.
- Concurrency: four simultaneous synthetic typed learner journeys passed; slowest complete journey 1.12 seconds in this instance. Disposable accounts were deleted. This is a local smoke test, not a production SLA or scalable capacity guarantee.
- Quality: Ruff, ESLint, Prettier, strict TypeScript, and Vite production build pass. CI configuration covers PostgreSQL migrations/tests, frontend tests/build, and Chromium journey. Hosted Actions execution is not established by local results.

Integration testing exposed and fixed the Vite proxy Host header and uncontrolled account form reuse. No failing assertion was removed to obtain these results.

Not verified: live Neon connection, paid transcription, calibrated pronunciation, real microphone hardware, consented diverse speech samples, qualified content/visual review, exhaustive accessibility, public HTTPS deployment, managed storage encryption, backup restore, SMTP delivery, or spending controls. These remain release gates. No overall proficiency or scoring-quality claim follows from code tests.

Commands: `pytest -q`; `ruff check backend scripts`; `ruff format --check backend scripts`; from frontend `npm run lint`, `npm run format:check`, `npm test`, `npm run build`, `CHROMIUM_PATH=/usr/bin/chromium npm run test:e2e`; `docker compose exec api python backend/manage.py check_speech_worker`; `python scripts/load_smoke.py`.

Final review also adds validation for non-object JSON/auth inputs and preserves typed-answer idempotency keys across network failures. The regression suite now contains 29 backend tests. Production staging HTTPS/static/API checks passed using its CA without insecure flags. The development-only staging mailer is an expected deployment blocker; it was not disabled or silenced to obtain a readiness claim.

A free offline PocketSphinx adapter adds two backend tests (31 total): real synthetic-command decoding and silence rejection. It is not a mock and needs no API credentials. Only the initial controlled command words were recognized reliably in the synthetic smoke; later words were misrecognized, so no accuracy/calibration claim is made. Paid transcription remains optional and untested.
