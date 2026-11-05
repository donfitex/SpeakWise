# SpeakWise AI

A structured English, pronunciation, diction, and elocution teacher. Lessons explain a concept, demonstrate it, invite practice, offer evidence-based feedback, and let the learner retry.

**Status:** Phase 01 foundation. Dependency installation is verified; the application is not implemented yet. See the [master plan](docs/master-plan.md) and [phase record](docs/phases.md).

## First release

Adult and older-teen self-study learners, pre-A1 through B1, using a small complete curriculum. Initial personas: a beginner practising everyday exchanges, an intermediate learner preparing clear introductions, and a learner refining a chosen pronunciation target. Child accounts, live group calls, exam certification, and B2–C2 coverage are later work.

Typed participation, captions, replay, keyboard access, and respectful feedback are core requirements. A transcript alone must never be used to diagnose pronunciation.

## Development setup today

Prerequisites verified in the cloud: Python 3.12 and Node 24 with npm 11. From the repository root:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pip check
cd frontend
npm install --package-lock=false
npm ls --depth=0
```

These commands install dependencies only. Django settings/manage.py, frontend source/tsconfig.json, and tests are planned in later phases. `npm run build` currently fails because tsconfig.json is missing; pytest currently collects no tests. Lockfiles and clean-install CI are scheduled for Phase 05. Until then, version ranges can resolve differently over time.

Copy `.env.example` to `.env` when configuring the upcoming local stack. Its variables are a planned configuration contract, not functioning application settings yet. Never put credentials in source or frontend environment variables. Docker Compose arrives in Phase 02, backend startup in Phase 03, and frontend startup in Phase 04.

## Repository map

- `backend/`: reserved for the Django modular monolith.
- `frontend/`: React/TypeScript dependency manifest; interface implementation follows.
- `requirements*.txt`: backend runtime and development dependencies.
- `docs/`: product plan, decisions, delivery evidence, and policies.

## Cost and data policy

Prefer free, open-source dependencies and local scripted teaching. Paid speech/AI services will be optional adapters, disabled without configuration; no paid account is needed for the planned local demonstration. Browser speech capabilities may vary and can use browser-vendor services; disclose that before enabling them. Do not promise free hosted production infrastructure.

Use synthetic lessons, fictional profiles, and generated test fixtures only. Do not commit real recordings, learner transcripts, personal information, or secrets. Raw audio retention defaults to off; meaningful speech scoring requires reviewed evidence and calibration, not code tests alone.

See [architecture decisions](docs/decisions/0001-foundation.md), [contributing](CONTRIBUTING.md), and [security reporting](SECURITY.md). Licensed under [Apache 2.0](LICENSE).
