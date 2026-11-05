# Pilot privacy and retention

This is an advisory pilot for self-attesting learners aged 16 and over; it is not a child-focused service. Jurisdiction-specific age eligibility and privacy obligations require review before launch. No legal compliance certification is claimed.

Collect account email/username, display name, optional language, preferences/goals, lesson answers and evidence needed for feedback. Do not infer identity, disability, intelligence, confidence, or effort from voice. Scripted teaching uses curated lesson text; no open-ended external model is enabled by default.

Microphone access is requested only after consent. Preview stays on-device until explicit upload. Submitted audio is private, limited to 2 MB/30 seconds, expires after ten minutes, and is removed after processing/failure. The scheduler purges expired files every five minutes. Revocation deletes pending recordings. No public media URL or raw replay history is offered.

Transcripts, turns, and answers are removed after 90 days of session inactivity by the daily purge. Derived skill notes are rebuilt from remaining evidence. Profile and consent history remain until account deletion. Owners can export active records, delete individual speech results, report feedback, or delete their account with password confirmation. No raw credentials/audio/transcript content is logged by application code. Operators must keep DEBUG off and configure log-access/rotation controls.

Production backups are an operator responsibility: set a documented maximum retention (recommended at most 30 days), restrict/encrypt access, and reapply account deletion records after restoration. Backups, external speech-provider retention, email service policies, and actual storage encryption must be verified for the chosen deployment before collecting real data. Default local development has no automated backup service. Do not claim backup erasure or provider deletion without evidence.
