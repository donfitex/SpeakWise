# API guide

Base path `/api/v1/`. OpenAPI is generated from explicit contracts and validated with `python backend/manage.py spectacular --validate --fail-on-warn`. Self-hosted Swagger UI is `/api/v1/docs/`; no external CDN is required. Requests use JSON objects unless noted. Session cookies stay same-origin; fetch `/auth/csrf/` first and send the csrftoken cookie as X-CSRFToken on unsafe requests. A login rotates the CSRF cookie, so reread it before the next write.

| Route | Contract |
| --- | --- |
| GET health/ | Database-backed `{status, service}` |
| POST auth/register/ | username, email, password, display_name, eligible (16+ pilot); returns profile, 201 |
| POST auth/login/ | username, password; returns profile, 200 |
| POST auth/logout/ | ends current session, 204 |
| POST auth/password-reset/ | email; non-enumerating status message |
| POST auth/password-reset/confirm/ | uid, token, password; single-use reset |
| GET/PATCH learners/me/ | own profile, goals, level, daily_minutes, pronunciation_model |
| GET/POST learners/me/consent/ | current audio consent; POST granted boolean |
| GET/DELETE learners/me/data/ | own export; deletion requires password and confirmation=DELETE, 204 |
| GET courses/ | published course/unit/lesson map in results; answer keys excluded |
| GET lessons/{version_id}/ | published explanation/objective/version/accessibility metadata |
| POST placement-sessions/ | begins owner-scoped text diagnostic, 201 |
| GET/POST placement-sessions/{id}/answers/ | POST index and answer; returns next question or advisory result |
| GET placement-sessions/{id}/result/ | same owner-scoped diagnostic state |
| POST lesson-sessions/ | lesson_version UUID, optional review boolean; new session 201, resume 200 |
| GET lesson-sessions/{id}/ | saved position, current activity, model, hints, and turns |
| POST lesson-sessions/{id}/turns/ | activity_id, answer, request_id UUID; session and attempt result |
| POST lesson-sessions/{id}/speech-attempts/ | multipart audio + request_id; returns queued private job, 202 |
| GET/DELETE speech-attempts/{id}/status/ | owner-only job/result; DELETE erases audio/transcript/result, 204 |
| GET speech-attempts/{id}/feedback/ | same owner-only status/feedback resource |
| GET learners/me/progress/ | per-skill controlled-task estimates/evidence/review dates |
| GET learners/me/recommendations/ | lesson_version or null, reason; title/review when present |
| GET learners/me/summary/ | completed lessons, attempts, real recorded seconds, resume links |
| GET learners/me/history/?page=N | paginated count/next/previous/results |
| POST assessments/{id}/report/ | reason, maximum 1000 characters; owner report, 201 |

Wrong/unknown user resources return 404. Unauthenticated/CSRF/permission denial returns 403 with session authentication; invalid input 400; stale/complete placement 409; throttle rejection 429. Field-validation errors may be a field-to-message mapping rather than a single detail string. Health may fail when the database is unreachable; provider jobs report failed state rather than fabricating results.

Reuse the same request_id when retrying the same answer/upload after transport failure. Reusing an answer key for different content is rejected. New voluntary retries get new keys. Validated task evidence records rubric version and explicitly says whether pronunciation was evaluated (currently false).

Authentication is limited to 10 requests/minute, ordinary anonymous API access 60/minute, authenticated API access 300/minute, and speech submission 20/hour. Local development uses a process-local cache; production uses shared Redis and still needs edge abuse controls. Staff authoring/review uses permission-controlled Django admin; no public staff write API is exposed.
