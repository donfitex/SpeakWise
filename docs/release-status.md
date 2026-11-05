# Release status

Code and documentation reached Phase 24. This is a working local pilot, **not a completed public production release**. The master plan's external/human acceptance criteria are tracked below rather than waived.

| Phase | State and evidence/remaining gate |
| --- | --- |
| 01 Foundation | Complete: scope, ADR, safe configuration, contribution/security guidance |
| 02 Local environment | Complete locally: six services built, HTTP/worker checks passed |
| 03 Backend | Complete locally: migrations, health, settings, API defaults |
| 04 Frontend | Complete locally: responsive routes/build; tested desktop/mobile states |
| 05 CI | Local gates pass; hosted Actions execution still needs confirmation |
| 06 Accounts | Implemented/tested; verified SMTP delivery and enrollment hardening remain release gates |
| 07 Curriculum | Implemented/tested; sample track only, not complete CEFR coverage |
| 08 Placement | Text diagnostic implemented; listening/speaking diagnostic remains open |
| 09 Sessions | Implemented/tested: ordered practice, retry, resume, completion, review |
| 10 Teacher | Scripted lesson-context teacher implemented; optional live LLM is not enabled |
| 11 Activities | Controlled core activity types implemented/tested; not open-ended proficiency grading |
| 12 Microphone | Capture/preview/consent implemented; real hardware/browser matrix still to review |
| 13 Providers | Interfaces/disabled/test mocks/free offline transcription implemented; paid provider untested |
| 14 Speech jobs | Real queue safe fallback/cleanup verified; free offline adapter tested separately; paid transcription unverified |
| 15 Pronunciation | Evidence/rubric/uncertainty safeguards implemented; calibrated evaluator and representative recording review are blockers |
| 16 Model voice | Browser local/opt-in online voice/captions/slow playback implemented; availability varies |
| 17 Visuals | Illustrative cues implemented; qualified English-language review remains open |
| 18 Adaptation | Tested controlled-text evidence and deterministic due-review reasons |
| 19 Dashboard | Implemented/tested owner history, resume, skill notes and next steps |
| 20 Content admin | Tested roles, draft clone, separate reviewer, audit, version preservation; actual educator approval still pending |
| 21 Hardening | Tested privacy/ownership/retention; legal/age review, backups, edge abuse and full manual accessibility remain open |
| 22 Pilot quality | Automated backend/frontend/browser/axe/queue/concurrency smoke passed; diverse speech calibration and human pilot not performed |
| 23 Deployment | Local production images/HTTPS smoke passed; live Neon, host/domain, email, private storage/backups/restore/spending controls remain external gates |
| 24 Portfolio | Documentation, fictional screenshots, case study, guides and known limits delivered; no public launch claimed |

Required next inputs: secure Neon DATABASE_URL and non-secret hostname/branch identification with permitted PostgreSQL/TCP access; chosen deployment host/domain and approved runtime credentials; verified email sender/transport; educator/reviewer availability and consented speech evaluation plan. Do not post credentials in chat. Optional paid speech remains disabled until explicitly configured with limits.

No cloud environment publication was performed during implementation. Separate conventional commits were pushed to main as requested. See phases.md for delivery notes and validation.md for commands/results.
