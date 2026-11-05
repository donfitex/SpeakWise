# ADR 0001: Learning-first modular monolith

Status: accepted for initial implementation.

Use Django REST Framework, React/TypeScript, PostgreSQL, and Redis/Celery when asynchronous work is introduced. Keep one backend deployment with domain modules for accounts, learners, curriculum, classroom, assessment, speech, progress, content administration, and notifications. Avoid independent services until operational evidence justifies them.

Store lesson objectives, state transitions, answer rules, rubrics, and progression in application logic and versioned content. Start with scripted teacher dialogue. Separate transcription, synthesis, and pronunciation interfaces; disabled and deterministic test providers are free defaults. Paid providers require explicit configuration and spending controls. ASR output is insufficient evidence for phoneme grading.

First track: adult/older-teen everyday English, pre-A1–B1. Initial lesson content is synthetic and must be reviewed before educational-quality claims. Do not add child-focused features or real learner data to a demo.

Use UUIDs for public records, explicit ownership, immutable historical content/rubric versions, minimal retention, and text alternatives. Default raw audio retention is off. Exact age eligibility, jurisdictional privacy obligations, deployment provider, and pronunciation evaluator remain release decisions; do not imply they have been reviewed.

Tradeoffs: a monolith is easier to operate and test, but background speech processing still requires worker lifecycle and retry design. PostgreSQL and Redis are free software, not a guarantee of free hosting. The current repository has dependency ranges without locks; Phase 05 will record reproducible resolutions and CI gates.
