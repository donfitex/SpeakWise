# Pilot threat model

Assets: credentials, session cookies, private audio, transcripts, assessments, curriculum history. Boundaries: browser/API, API/database, queue/worker, optional speech vendor, staff admin.

Controls: password validation/hashing, CSRF including anonymous auth writes, secure production cookies/headers, owner-filtered resource lookup, request limits, shared production throttling, private media with no web route, worker-side decode/duration checks, least-privilege staff permissions, immutable historical content, separate reviewer, evidence/uncertainty constraints, consent/revocation/expiry/deletion, no raw payload logging, and server-only provider keys.

Residual risks/release gates: distributed abuse requires edge rate limiting; no verified email enrollment; school/child use is unsupported; pronunciation calibration and educator review are pending; PostgreSQL/TLS/private storage/backup restore and Neon credentials must be verified; uploaded media decoders and dependencies need security patching; browser voice vendors may process disclosed model phrases. Production TLS termination, CSP, monitoring, incident contacts, and spending limits need operator configuration. Avoid real learner data until these gates are reviewed.
