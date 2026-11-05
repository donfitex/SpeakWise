# SpeakWise: from dependency manifests to a guided learning pilot

## Problem and design

The starting repository contained Python and frontend dependency manifests without application entry points. The product needed a structured teaching loop with transparent feedback rather than an unbounded chatbot. The initial audience is adult/older-teen self-study learners from pre-A1–B1, with a deliberately small sample track.

The implementation stores objectives, references, rubrics, versions, and progression in Django. A scripted teacher explains, waits, responds, and offers a retry. React presents a calm classroom with a typed path, optional recording, captions, and model playback. Adapters keep transcription separate from pronunciation evaluation so ASR cannot masquerade as phoneme scoring.

## Engineering decisions

A modular monolith keeps deployment and ownership checks tractable. Session authentication and CSRF fit a same-origin application. UUID domain records, owner-scoped queries, idempotent submissions, immutable published versions, a separate content reviewer, and explicit uncertainty support explainable history. Neon is the selected hosted PostgreSQL option, with local PostgreSQL for offline development and CI.

Free local defaults keep the pilot usable without provider credentials. Raw audio is private, bounded, and removed after processing; a scheduler handles expiry and inactive-session retention. Production images use non-root API processes, private service networking, Caddy HTTPS, and self-hosted API docs.

## Evidence and lessons

The recorded automated checks include 31 backend tests, four frontend behavior tests, two real Chromium journeys, tested-state axe scans, PostgreSQL migration/behavior checks, real Celery delivery, and four concurrent synthetic typed journeys. Browser testing caught a proxy host mismatch and React uncontrolled-field reuse; production staging caught copied-file ownership and internal reverse-proxy routing. These were fixed and affected checks rerun.

Local staging verified TLS using its CA rather than disabling verification. It correctly exposed the development mailer's production-check failure. No live Neon, public deployment, SMTP delivery, representative speech calibration, or full human accessibility review is claimed.

## Screenshots and data

The [desktop dashboard](screenshots/dashboard-desktop.png) and [mobile dashboard](screenshots/dashboard-mobile.png) use fictional “Sample Learner” data from the browser test. No real learner audio, transcript, account, or credential is included.

## Release boundary

The result is a reviewable local pilot with documented operational and educational gates. A calibrated pronunciation evaluator, reviewed curriculum/visuals, live Neon configuration, host/domain, email, private production storage/backups/restore, legal/age review, and a consented diverse pilot are needed before stronger release claims. See release-status.md for every phase's actual state.
