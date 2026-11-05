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

## Phase 07 — Course and content data model

Added UUID course/unit/lesson/version/skill/activity/rubric models, draft visibility, published-content immutability, safe public lesson representations (no answer keys), and idempotent synthetic demo seeding across pre-A1–B1. Four backend tests pass, including repeated seeding, hidden drafts, and immutable published prompts. The sample track is deliberately small and marked as awaiting educational review, not complete CEFR coverage.

## Phase 08 — Learner onboarding and placement

Added goals/level preferences, a four-question text diagnostic with server-controlled sequencing, owner-only results, low-confidence evidence, and learner override. Five backend tests and frontend lint/build pass. Listening and speaking placement are explicitly unmeasured; the full multimodal diagnostic acceptance gate remains open pending reliable speech services and reviewed content.

## Phase 09 — Lesson session engine

Added prerequisite checks, published-version access, persisted owner-only sessions, ordered activities, retry without advancement, idempotent answer keys, and completion timestamps. Six tests pass, including resume, duplicate submission, key misuse, and cross-user denial. Controlled text matching measures task completion only; no pronunciation or open-ended proficiency claims are made.

## Phase 10 — Text-based classroom teacher

Connected the course map to saved sessions and added scripted teacher explanation, one-at-a-time prompts, contextual hints, feedback, retry, and persisted teacher/learner turns. Six backend tests pass with turn persistence and no duplicate turns on replay; frontend lint/build pass. This is a deterministic scripted teacher, not an enabled language-model conversation service.

## Phase 11 — Core English activities

Added task-specific guidance and evidence for grammar, vocabulary, listening-with-caption, reading, sentence building, controlled writing, and typed speaking practice. Thirteen backend tests pass, including each activity type, normalization, positive reference matching, and retry guidance. Open-ended writing and actual listening/speaking proficiency grading are not inferred from controlled text matching.

## Phase 12 — Microphone capture and audio playback

Added consent-before-capture, 30-second recording, local preview, track cleanup, cancel/discard/retry, device selection after permission, typed fallback, and permission/device errors. Two frontend behavior tests plus lint/build pass. Capture is local until an explicit submit action; asynchronous upload is added in Phase 14. Real microphone hardware and browser support still require pilot verification.

## Phase 13 — Speech service adapters

Added separate transcription, synthesis, pronunciation, and alignment protocols, disabled defaults, explicit test-only mock, and optional OpenAI transcription adapter with timeout/failure fallback. Sixteen backend tests pass. No paid provider is enabled or live-tested; calibrated pronunciation and server TTS remain unavailable and report that honestly.

## Phase 14 — Asynchronous speech processing

Added consent/ownership checks, private bounded uploads, idempotent jobs, worker-side audio decoding/duration validation, status polling, transcript deletion, provider fallback, and expiry cleanup. Eighteen backend tests and two frontend tests pass, including synthetic WAV decoding, malformed media, duplicate jobs, expiry, and access denial. Raw audio is removed after processing or failure. Live provider transcription remains unverified; disabled provider fails safely and typed practice remains available.

## Phase 15 — Pronunciation and elocution feedback

Added versioned assessment evidence, rubric-bound dimension validation, uncertainty/mock suppression, and owner-only feedback reporting. Twenty backend tests pass; out-of-range/unknown dimensions are rejected and weak evidence never produces a score. No calibrated pronunciation evaluator exists, so pronunciation, stress, pace, and intonation scoring remain an explicit release gate; code cannot honestly establish scoring quality without reviewed recordings.

## Phase 16 — Audio teacher and model examples

Added user-triggered browser model speech with caption, local-English-voice preference, optional disclosed online voices, normal/slow playback, stop, voice selection, and text fallback. Three frontend behavior tests plus lint/build pass. Model phrases only are synthesized; real browser voice availability varies and no server TTS provider is configured.

## Phase 17 — Visual pronunciation tools

Added reference-specific syllable/stress blocks, pause/intonation guidance, and a simplified closed-lip /m/ illustration with text alternatives. Twenty-one backend tests and frontend lint/build pass. Cues are visibly labelled illustrative and unreviewed; qualified English-language review is still required to satisfy the educational-review acceptance gate.

## Phase 18 — Adaptive feedback and learning plan

Added per-skill recent controlled-task estimates, evidence counts, 1/3/7-day review rules, reproducible recommendation reasons, preferred-level selection, and repeat review sessions. Twenty-two backend tests pass; reprocessing evidence does not inflate counts, and typed speech/listening does not claim mastery. Estimates are advisory and are not a CEFR qualification or calibrated speech score.

## Phase 19 — Dashboard and learning history

Added authenticated home/progress dashboard, completed lesson and attempt counts, actual recorded practice duration, resume links, recommendation reasons, skill evidence/review dates, paginated history, and feedback reporting UI. Twenty-three backend tests and frontend lint/build pass. No invented streak, typed practice time, or single mastery score is shown. Owner isolation and history pagination are tested.

## Phase 20 — Content authoring and review

Added staff administration, draft cloning, read-only submitted/published versions, activity/rubric editing, separate-reviewer publication, archival, and audit records. Twenty-four backend tests pass, including unauthorized author denial, self-review denial, stale-instance edit rejection, and historical version preservation. Admin forms provide content preview; qualified educational review and actual staff assignment remain release tasks.

## Phase 21 — Privacy, safety, and accessibility hardening

Added consent revocation that stops/deletes pending audio, owner data export, password-confirmed account deletion with file cleanup, 90-day inactive-session purge, scheduler service, shared production throttling, and privacy/threat-model documentation. Twenty-five backend tests plus three frontend tests and frontend lint/build pass. Browser accessibility checks follow in Phase 22; deployment backups, jurisdictional review, and verified email/edge-abuse controls remain release gates.

## Phase 22 — Integration tests and pilot quality

Added real Chromium journey/axe desktop/mobile/keyboard checks, recording lifecycle test, PostgreSQL test option, live worker smoke command, four-user concurrent typed smoke, and hosted journey CI configuration. 28 backend tests, four frontend tests, two browser tests, and live worker/concurrency checks pass. Browser testing found and fixed proxy Host handling and reused form fields. See validation.md. Diverse consented speech evaluation, scoring calibration, educator review, and full manual accessibility remain open pilot-release gates.

## Phase 23 — Deployment and operations

Added production Gunicorn/Caddy images and Compose, verified local internal TLS health/static responses, private API/Redis networking, resource caps, security headers, collected static assets, self-hosted OpenAPI UI, validated API contracts, mailer modernization, and deployment/backup/incident/spending runbook. Fixed non-root copied-source ownership and internal proxy routing found during staging. Local staging uses local PostgreSQL only. Public deployment, live Neon, SMTP delivery, managed private storage/backups and restore are not complete; staging's development mailer correctly fails the deployment email gate. No cloud environment was published and no paid infrastructure was provisioned.
