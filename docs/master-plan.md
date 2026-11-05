# SpeakWise AI
## Codex Master Plan: English Language, Pronunciation, Diction, and Elocution Teacher

**Product type:** Adaptive, classroom-style English learning platform  
**Primary stack:** Python, Django REST Framework, React, TypeScript, PostgreSQL  
**Delivery approach:** Build and review one tested phase at a time; keep each phase in a separate Git commit.

> **Project goal:** Build an approachable AI teacher that teaches English through structured lessons, spoken and typed interaction, visual demonstrations, practice, assessment, and personalized follow-up. It should help a learner understand what to improve and give them a practical next exercise.

## 1. Product vision

SpeakWise AI is a digital English teacher for learners with different starting points and goals. It combines a guided curriculum with a conversational tutor. The tutor teaches, asks questions, listens to the learner, gives focused feedback, and adapts practice based on evidence from earlier lessons.

The app is not an unstructured chatbot. Lesson objectives, examples, practice activities, assessment rubrics, and progression rules are stored as product content. The AI explains and personalizes that material within those boundaries.

### Product principles

- **Teach in small steps.** Explain one concept, demonstrate it, practise it, check understanding, and revisit it later.
- **Make feedback actionable.** Show the learner what happened and what to try next, in supportive language.
- **Evaluate fairly.** Assess intelligibility and task performance. Do not treat a learner's identity, home language, or accent as a defect. Let learners choose a target pronunciation model where relevant.
- **Offer more than one way to participate.** Support microphone, typed responses, captions, replay, and text explanations.
- **Adapt from evidence.** Use lesson attempts, skill scores, confidence, and learner goals to choose follow-up lessons. Do not make unexplained jumps in difficulty.
- **Protect learners.** Collect only necessary data, explain audio handling, and provide deletion controls. Use age-appropriate content and safeguards for young learners.

### First release scope

The first release should serve adult and older-teen self-study learners from pre-A1/novice through B1/intermediate, with a small, complete curriculum in pronunciation, everyday English, listening, grammar, vocabulary, and speaking. Design the content model so child, school, exam-preparation, and professional tracks can be added later. Do not claim that the initial release fully covers every age, syllabus, or English examination.

## 2. Learners, levels, and goals

Use a familiar level ladder and explain it in plain English. A placement activity should recommend a starting point, not permanently label the student. Learners can choose a different level and ask for reassessment.

- **Novice / pre-A1:** alphabet and sounds, basic classroom language, greetings, simple words and phrases.
- **Beginner / A1:** familiar expressions, simple questions and answers, core sentence patterns, pronunciation foundations.
- **Elementary / A2:** everyday exchanges, short descriptions, common grammar, listening for key information.
- **Intermediate / B1:** connected speech, longer conversations, common writing tasks, clearer presentations.
- **Upper-intermediate / B2:** nuance, argument, extended listening, professional communication and structured speaking.
- **Advanced / C1:** precise language, register, complex texts, persuasive presentations, pronunciation refinement.
- **Proficient / C2:** flexible expression and advanced communication goals; offer this after the first release.

### Learner goals

Allow learners to choose one or more goals: speak confidently in daily life, improve pronunciation, practise diction, improve grammar, prepare for interviews, communicate at work, speak in public, improve listening, or prepare for a named examination. Examination tracks must identify the relevant syllabus and version instead of making generic promises.

### Age and context tracks

Store a learner's age band and learning context only when needed. Use those settings to choose examples, reading difficulty, content safeguards, and tone. Keep child profiles and guardian/teacher controls as a later release unless the project explicitly targets children from the start.

## 3. Teaching method and classroom experience

A learner should feel that a patient teacher is guiding a lesson, not that they are submitting isolated prompts to a bot.

### Lesson loop

1. **Welcome and goal:** The teacher states the lesson objective and connects it to the learner's goal.
2. **Explain:** Present a short explanation with a written example, audio model, and visual cue where useful.
3. **Demonstrate:** Read the phrase or sentence aloud, show a transcript, and draw attention to the relevant sound, stress, grammar point, or meaning.
4. **Guided practice:** Ask a question or request a spoken/typed response. Wait for the learner before continuing.
5. **Feedback:** Identify one success and one or two specific corrections. Show a corrected example and let the learner replay it.
6. **Retry:** Give the learner an immediate chance to repeat or apply the correction in a new sentence.
7. **Check and adapt:** Score the attempt, update the skill record, and choose the next exercise or review.
8. **Close:** Summarize the lesson and give a short independent practice task.

### Classroom modes

- **Private lesson:** One learner and the AI teacher, with turn-taking and a visible lesson board.
- **Practice room:** Repeat-after-me, minimal pairs, read-aloud, listening, vocabulary, grammar, and role-play activities.
- **Classroom simulation:** The AI teacher asks a question, the learner answers, receives feedback, and is invited to respond again. Version one can simulate a class without live group calls.
- **Group classroom (later):** Teacher-led sessions with multiple learners, turn management, educator controls, and moderated participation.

### Visual and audio teaching tools

- Microphone permission flow, input-device selection where supported, recording indicator, playback, and retry.
- Synchronized text transcript with phrase- or word-level highlighting when alignment data is available.
- Syllable blocks, stress marks, intonation arrows or pitch contours, and phoneme targets.
- Mouth-position illustrations for selected sounds, with plain-language articulation tips.
- Slow and normal-speed model audio, replay, captions, and optional phonetic transcription.
- Visual progress indicators for the skill being practised; avoid decorative scores that do not explain learning.

Do not require camera access for the core experience. A camera-based articulation feature can be considered later only with a clear learner benefit, explicit consent, and a privacy review.

## 4. Core product modules

### A. Learner onboarding and placement

Collect display name, language-learning background, level preference, goals, available practice time, age band if necessary, and target pronunciation model if the learner wants one. Use a short diagnostic across listening, vocabulary, grammar, reading, and speaking. Return a suggested level with evidence and a confidence note.

### B. Curriculum and lesson library

Organize content as courses, levels, units, lessons, objectives, concepts, examples, activities, answer keys, rubrics, and prerequisites. Every lesson has an estimated duration, accessibility notes, required media, target skills, and a clear completion rule. Content should be versioned so changes do not silently rewrite historical assessment meaning.

### C. AI teacher and lesson orchestration

The teacher follows the active lesson plan, uses the learner's profile and progress, asks one question at a time, waits for the answer, and chooses a relevant hint or next step. It may simplify its explanation, provide another example, or recommend a review. Keep lesson state and grading rules in application logic; use the language model for explanation and conversational phrasing within those rules.

### D. Speaking, pronunciation, diction, and elocution

Teach sound contrasts, word stress, syllables, connected speech, rhythm, pausing, pace, emphasis, and intonation. Include read-aloud, recitation, storytelling, interviews, introductions, presentations, and impromptu speaking activities. Let the learner choose a practice target such as British, American, or another supported model. The teaching objective is clear communication, not accent erasure.

### E. Assessment and feedback

Use task-specific rubrics. Feedback should identify the observed issue, show a model, explain one practical adjustment, and provide a retry. Separate objective measures from approximate AI judgments. If audio quality is poor or the evaluator is uncertain, say so and offer another recording or a typed alternative.

### F. Adaptive learning plan

Maintain a skill map for areas such as phoneme contrasts, word stress, sentence stress, listening comprehension, grammar topics, vocabulary, fluency, and presentation structure. Recommend review based on recent performance, repeated error patterns, and spaced practice. Let learners see why an activity was recommended.

### G. Learner dashboard

Show current course, lessons completed, time practised, skill progress, recent feedback, next recommended activity, and personal goals. Use clear trends; avoid presenting a single score as a complete measure of English ability.

### H. Teacher/content administration

Provide authorized staff with tools to create, edit, review, publish, archive, and version lessons and rubrics. Include draft status, content review notes, accessibility fields, and a preview of each activity.

## 5. Assessment rubric and AI behavior

### Suggested speaking rubric

Score only dimensions that the task can reasonably measure. Use a transparent rubric, for example 1–5 levels with descriptions and evidence.

- **Task completion:** Did the learner answer or perform the requested task?
- **Intelligibility:** Could a listener understand the words and message?
- **Target sound practice:** How accurately did the learner produce the specific sound or contrast taught in the exercise?
- **Word and sentence stress:** Did emphasis help communicate the intended words and meaning?
- **Pace and pausing:** Was the speech rate manageable and appropriately paused?
- **Intonation:** Did pitch movement support the intended question, statement, or emphasis?
- **Grammar and vocabulary:** Were structures and words appropriate for the task and current level?
- **Listening comprehension:** Did the response show understanding of the prompt or audio?

Do not infer a learner's confidence, personality, intelligence, or effort from voice characteristics. Do not rank accents as better or worse. Accent-target feedback should only compare the learner's practice to a target they selected, while preserving intelligibility as the main communication goal.

### Confidence and fairness rules

- A speech-to-text transcript is not enough to diagnose pronunciation. Use a pronunciation-capable evaluation method for phoneme-level feedback; use ASR as a supporting signal, not the sole judge.
- Keep the reference phrase or expected response for controlled speaking exercises so results are comparable.
- Calibrate scores against reviewed sample recordings representing different voices, ages, English varieties, microphones, and noise levels before using them for meaningful progression.
- Return a confidence estimate or “not enough evidence” when audio, alignment, or model output is weak.
- For open-ended speaking, assess meaning and communication with a level-appropriate rubric; avoid false claims of precise pronunciation diagnosis.
- Store score evidence and rubric version so learner history remains explainable after content changes.
- Provide a learner retry and an appeal/report option for feedback they believe is inaccurate.

### Example feedback

**Observed:** “ship” sounded closer to “sheep” in this attempt.  
**Try:** Keep the vowel shorter and more relaxed. Listen to both examples, then repeat “ship” in the sentence.  
**Confidence:** Medium. Background noise was noticeable; replay or record again for a more reliable result.

## 6. Technical architecture

Build a modular monolith for the first release. Keep speech services behind replaceable provider interfaces so the app can switch vendors, run a limited local option, or disable a feature without rewriting lessons and learner records.

### Recommended stack

- **Backend:** Python, Django, Django REST Framework, Django ORM, PostgreSQL.
- **Frontend:** React, TypeScript, accessible component system, responsive web app/PWA.
- **Background jobs:** Celery and Redis for audio processing, lesson reports, and scheduled review reminders.
- **Audio:** Browser microphone capture and playback; use recording support with graceful permission/device error states. Use speech-to-text, text-to-speech, and pronunciation evaluation through separate service adapters.
- **Media storage:** Private object storage for any audio retained beyond a request. Default to short-lived processing and minimal retention. Store references and metadata in PostgreSQL, not large audio blobs.
- **Operations:** Docker Compose for local services; GitHub Actions for CI; one deployable web API, one worker, a frontend, managed PostgreSQL, and Redis where available.
- **Later mobile app:** Reuse the API from a dedicated Android client after the web learning loop is stable.

### Service boundaries

- `accounts`: users, authentication, roles, consent settings.
- `learners`: learner profile, goals, preferences, accessibility.
- `curriculum`: courses, levels, lessons, activities, rubrics, content versions.
- `classroom`: lesson sessions, turn state, teacher messages, learner answers.
- `assessment`: attempts, scoring, evidence, confidence, review state.
- `speech`: upload/recording metadata, transcription jobs, TTS and evaluation adapters.
- `progress`: skill map, mastery estimates, recommendations, review schedule.
- `content_admin`: authoring, moderation, publishing workflow.
- `notifications`: reminders and email preferences.

## 7. Initial data model

Use UUID primary keys for externally referenced records. Add `created_at` and `updated_at` where appropriate. Use explicit ownership and permissions rather than trusting client-supplied IDs.

- `User`: account credentials and role flags.
- `LearnerProfile`: user, age band if required, first language (optional), level preference, locale, accessibility preferences.
- `LearnerGoal`: learner, goal type, target date (optional), status.
- `ConsentRecord`: learner/user, consent type, policy version, granted/revoked timestamps; do not store unnecessary personal data.
- `Course` and `CourseVersion`: title, audience, target levels, status, version.
- `Unit`, `Lesson`, `LessonVersion`: objective, prerequisites, sequence, estimated time, content status.
- `Skill` and `LessonSkill`: skill taxonomy and lesson-to-skill links.
- `Activity`: type, prompt, reference response/audio, expected answer rules, rubric, media references.
- `LessonSession`: learner, lesson version, current state, started/completed timestamps.
- `ActivityAttempt`: session, activity, text answer, result, attempt number, time taken.
- `SpeechAttempt`: activity attempt, private audio reference (optional), duration, retention expiry, transcript status, consent reference.
- `AssessmentResult`: attempt, rubric version, dimension scores, evidence, confidence, evaluator version.
- `SkillProgress`: learner, skill, current estimate, evidence count, last practiced, next review due.
- `TeacherTurn`: session, speaker, content, activity reference, created time; keep only what is useful and retention-controlled.
- `ContentReview`: lesson version, reviewer, status, notes, timestamp.

## 8. API outline

Use a versioned REST API under `/api/v1/`. Document request/response shapes and error codes with OpenAPI.

- `POST /auth/register/`, `POST /auth/login/`, `POST /auth/logout/`, `POST /auth/password-reset/`
- `GET/PATCH /learners/me/` for learner profile and preferences.
- `GET /courses/`, `GET /courses/{id}/units/`, `GET /lessons/{id}/`
- `POST /placement-sessions/`, `POST /placement-sessions/{id}/answers/`, `GET /placement-sessions/{id}/result/`
- `POST /lesson-sessions/`, `GET /lesson-sessions/{id}/`, `POST /lesson-sessions/{id}/turns/`
- `POST /activities/{id}/attempts/` for text/choice responses.
- `POST /activities/{id}/speech-attempts/` for authorized audio submission; return a job/status resource.
- `GET /speech-attempts/{id}/status/`, `GET /speech-attempts/{id}/feedback/`
- `GET /learners/me/progress/`, `GET /learners/me/recommendations/`, `GET /learners/me/history/`
- Staff-only endpoints for lesson drafts, rubric versions, review, publication, and archival.
- `DELETE /learners/me/audio/{id}/` and account/data deletion workflow where required by retention policy.

Enforce permissions on every route. Validate lesson access and audio ownership server-side. Paginate lists and rate-limit authentication and costly speech operations.

## 9. User interface map

1. **Welcome and sign-up:** product explanation, age-appropriate setup, privacy and audio consent.
2. **Goal and level setup:** goal selection, target variety, placement recommendation.
3. **Home dashboard:** next lesson, skills, progress, practice reminder settings.
4. **Course map:** levels, units, locked/unlocked states, expected outcomes.
5. **Lesson classroom:** teacher panel, visual board, captions, activity, microphone/typing controls, replay and hints.
6. **Speaking feedback:** transcript, target word/sound, rubric, confidence, retry action.
7. **Progress report:** skill map and understandable recommendations.
8. **Content admin:** lesson authoring, review queue, preview, publish/retire.

Every screen must include loading, empty, error, offline/unsupported, permission-denied, and retry states where relevant. Provide keyboard navigation, readable contrast, captions, text alternatives, and a typed path for learners who cannot or do not wish to speak aloud.

## 10. Security, privacy, and learner wellbeing

- Use secure authentication, CSRF protections where applicable, HTTPS, strict CORS, secure headers, rate limits, and environment-managed secrets.
- Ask for microphone access only when needed and explain what will happen to recordings.
- Default to not retaining raw audio after evaluation unless the learner has explicitly opted in for replay/history. Provide an expiry and deletion process.
- Encrypt transport and storage; restrict audio access to the owner and authorized staff; issue short-lived download links if needed.
- Never log raw audio, credentials, access tokens, or full learner transcripts by default. Redact application logs and support requests.
- Define a retention schedule and deletion behavior for recordings, transcripts, account data, backups, and derived assessments.
- If serving children, add guardian/teacher consent and controls, age-appropriate lessons, moderated AI output, safe interaction boundaries, and a formal child privacy review before launch.
- Keep an incident response and data-access process. Do not claim compliance with a law or certification unless reviewed and verified for the actual deployment.
- Provide respectful feedback; do not shame, stereotype, or penalize disability-related speech. Offer accommodations and alternate activity modes.

## 11. Phased implementation plan and Git commits

Complete one phase at a time. Each phase should have code, documentation, and tests appropriate to its scope. Proposed commit messages use `<type>(<scope>): <subject>`.

### Phase 01 — Product and repository foundation

**Work:** Inspect the repository; document product scope, learner personas, initial content track, architecture decisions, code style, `.gitignore`, README, `.env.example`, and contribution workflow. Establish backend/frontend folders.  
**Done when:** A clean checkout explains the goal, setup, synthetic/demo content policy, and planned boundaries. No secrets are tracked.  
**Commit:** `chore(scaffold): initialize speakwise project`

### Phase 02 — Local developer environment

**Work:** Add Docker Compose for PostgreSQL, Redis, Django API, worker, and frontend; add health checks, environment loading, persistent local volumes, and startup instructions.  
**Done when:** A new developer can start the development stack using documented commands.  
**Commit:** `chore(devx): add local docker compose stack`

### Phase 03 — Backend foundation

**Work:** Create Django project, modular apps, settings split, API prefix, PostgreSQL configuration, logging baseline, health endpoint, and initial migrations.  
**Done when:** API starts, migrations apply, checks pass, and no secrets are embedded.  
**Commit:** `feat(api): create django rest foundation`

### Phase 04 — Frontend foundation and design system

**Work:** Create React/TypeScript app, strict type checking, routing, accessible layout, design tokens, API client, responsive navigation, and shared UI states.  
**Done when:** Frontend builds and routes display correctly at mobile and desktop sizes.  
**Commit:** `feat(web): scaffold typed learning interface`

### Phase 05 — CI and code quality

**Work:** Configure backend lint/format/test checks, frontend lint/type-check/build, dependency lockfiles, and GitHub Actions. Add pull request template and review checklist.  
**Done when:** CI runs on pull requests and fails on a deliberately failing check.  
**Commit:** `ci(github): add project quality workflow`

### Phase 06 — Accounts and learner profile

**Work:** Implement registration/login/logout/password reset baseline, learner profile, preferences, goals, and audio consent record.  
**Done when:** Authenticated users can manage their own profile; tests deny cross-user access.  
**Commit:** `feat(accounts): add learner accounts and profiles`

### Phase 07 — Course and content data model

**Work:** Add course, level, unit, lesson, skill, activity, rubric, draft/published status, and content versioning. Add small sample lessons.  
**Done when:** Content relationships validate; published lessons can be read; edits create trackable versions.  
**Commit:** `feat(curriculum): model courses lessons and skills`

### Phase 08 — Learner onboarding and placement

**Work:** Build goal selection, self-selected level, short placement activities across multiple skills, result explanation, and recommendation.  
**Done when:** Placement recommends a starting level with evidence and lets a learner choose another level.  
**Commit:** `feat(placement): add learner diagnostic flow`

### Phase 09 — Lesson session engine

**Work:** Implement lesson state, activity sequencing, prerequisites, save/resume, answer recording, and completion rules.  
**Done when:** A learner can start, pause, resume, and complete a lesson without losing progress.  
**Commit:** `feat(lessons): add guided lesson sessions`

### Phase 10 — Text-based classroom teacher

**Work:** Build the teacher panel and turn-taking classroom using scripted content first: explanations, questions, hints, examples, and feedback templates.  
**Done when:** Teacher asks one question at a time, waits for an answer, responds in lesson context, and records turns.  
**Commit:** `feat(classroom): add interactive teacher dialogue`

### Phase 11 — Core English activities

**Work:** Add grammar, vocabulary, listening comprehension, reading, sentence building, and writing activities with answer keys and level-specific feedback.  
**Done when:** Each activity type has validation, feedback, completion state, and tests.  
**Commit:** `feat(activities): add core english practice types`

### Phase 12 — Microphone capture and audio playback

**Work:** Add microphone permission flow, recording controls, playback, cancellation, retry, duration limits, typed alternative, and accessible permission/device error states.  
**Done when:** Learner can record a bounded response, review it, discard it, or submit it after consent.  
**Commit:** `feat(audio): add learner recording and playback`

### Phase 13 — Speech service adapters

**Work:** Define provider interfaces for speech-to-text, text-to-speech, pronunciation evaluation, and optional alignment. Add a mock implementation for local tests and configuration for one selected provider.  
**Done when:** Provider can be replaced without changing lesson/domain logic; failures have safe fallback behavior.  
**Commit:** `feat(speech): add replaceable audio service adapters`

### Phase 14 — Transcription and speech activity processing

**Work:** Add asynchronous speech jobs, status polling, transcript handling, retries, file cleanup, limits, and basic pronunciation exercise data flow.  
**Done when:** A recording receives a job status and transcript/result; retries do not duplicate attempts; expired audio is deleted.  
**Commit:** `feat(speech): process speaking attempts asynchronously`

### Phase 15 — Pronunciation and elocution feedback

**Work:** Implement controlled-reference tasks for target sounds, word stress, pacing, pausing, and intonation; record dimension-level evidence and confidence.  
**Done when:** Feedback is tied to the task and rubric, uncertain scores are flagged, and learners can retry.  
**Commit:** `feat(assessment): evaluate pronunciation practice`

### Phase 16 — Audio teacher and model examples

**Work:** Add text-to-speech for lesson prompts and examples, replay/slow playback where supported, captions, and voice settings.  
**Done when:** Learners can hear model phrases with the transcript and fallback to text if audio generation fails.  
**Commit:** `feat(voice): add spoken lesson examples`

### Phase 17 — Visual pronunciation tools

**Work:** Add syllable segmentation, stress marks, intonation visualization, phoneme target highlights, and reviewed mouth-position illustrations.  
**Done when:** Visual cues correspond to lesson targets, include text alternatives, and are checked by an English-language reviewer.  
**Commit:** `feat(visuals): add pronunciation learning aids`

### Phase 18 — Adaptive feedback and learning plan

**Work:** Build the skill map, progress evidence, retry rules, spaced review recommendations, learner-facing reason for each recommendation, and transparent rubric display.  
**Done when:** Scores update only from valid evidence; next steps are reproducible and visible to learner.  
**Commit:** `feat(progress): personalize lesson recommendations`

### Phase 19 — Dashboard and learning history

**Work:** Build home dashboard, course map, recent attempts, strengths, focus skills, streak/practice time where meaningful, and history views.  
**Done when:** Learner can understand progress without interpreting a single overall score as mastery.  
**Commit:** `feat(dashboard): show learner progress and next steps`

### Phase 20 — Content authoring and review workflow

**Work:** Add staff role, content editor, rubric editor/versioning, preview, review/approval, publish, archive, and audit history.  
**Done when:** Unauthorized users cannot edit content; published changes are versioned and traceable.  
**Commit:** `feat(admin): add lesson authoring and review`

### Phase 21 — Privacy, safety, and accessibility hardening

**Work:** Add deletion/retention workflows, sensitive data redaction, rate limits, age-appropriate behavior controls for chosen audience, accessibility audit, and threat model.  
**Done when:** Privacy rules are tested; key paths have keyboard, screen-reader, caption, and text-only alternatives.  
**Commit:** `fix(security): harden learner privacy and audio handling`

### Phase 22 — Integration tests and pilot quality

**Work:** Test complete learner journeys, roles, service failures, poor audio, diverse speech samples with consent, scoring consistency, accessibility, and load within declared pilot limits.  
**Done when:** Core journey works from clean setup; failures and uncertain evaluations produce clear recovery paths.  
**Commit:** `test(e2e): cover learner teaching journey`

### Phase 23 — Deployment and operations

**Work:** Deploy frontend, Django API, worker, PostgreSQL, Redis, and private audio storage; configure HTTPS, secrets, health checks, migrations, backups, logs, and spending limits.  
**Done when:** Deployed demo works, no credentials are in source, and operator knows how to restore data and disable a speech provider.  
**Commit:** `deploy(platform): deploy speakwise learning app`

### Phase 24 — Portfolio release and documentation

**Work:** Add user guide, course/content guide, architecture diagram, API docs, privacy statement, demo account/data, known limitations, screenshots, and short case study.  
**Done when:** Another developer can run and review the project; demo uses no real learner audio or personal data.  
**Commit:** `docs(portfolio): publish speakwise case study`

## 12. Testing and release gates

- **Curriculum tests:** level prerequisites, content versioning, valid activities, rubric references, answer key behavior.
- **API tests:** authentication, ownership, permissions, validation, pagination, error formats, and rate limits.
- **Lesson engine tests:** resume behavior, retries, completion rules, and recommendation determinism.
- **Audio tests:** consent enforcement, file type/size/duration limits, expired file deletion, job failure/retry, provider timeout, and no raw audio in logs.
- **Assessment tests:** rubric dimension bounds, evidence exists, low confidence handling, no score when evidence is inadequate, and consistent retry workflow.
- **Frontend tests:** microphone states, typed fallback, accessible labels, transcript display, progress, loading/error/empty states.
- **End-to-end tests:** sign up, choose a goal, complete a lesson, record or type an answer, receive feedback, retry, and see next recommendation.
- **Quality gates:** lint, type-check, tests, migration check, dependency review, accessibility checks, build, and deployment smoke test.

Do not claim scoring quality from code tests alone. Before release, review scoring against representative speech samples with qualified English educators and speakers of supported varieties. Keep any pilot scoring advisory until evidence supports stronger claims.

## 13. Codex agent operating prompt

> You are the implementation agent for SpeakWise AI, a structured English and elocution teaching platform. Read repository instructions and inspect the current code before changing files. Preserve user work. Follow this master plan in phase order and implement only the next unfinished phase unless the user asks for a larger scope. Do not skip acceptance criteria.
>
> Before coding, state the phase, current repository status, proposed changes, files likely to change, and checks to run. Implement a vertical slice with understandable code and appropriate tests. Use synthetic/sample content only. Never hard-code secrets or commit real voice recordings, learner transcripts, or personal data.
>
> Keep speech-to-text, text-to-speech, and pronunciation evaluation behind separate provider interfaces. Never treat a transcript alone as proof of correct pronunciation. Return uncertainty when audio quality or evaluator confidence is insufficient. Keep scores tied to versioned rubrics and evidence. Provide text and replay alternatives.
>
> Every endpoint and background task must enforce learner ownership and role permissions server-side. Protect audio with consent, minimum retention, access controls, and deletion. Do not add child-focused features without age-appropriate content and guardian/teacher safeguards.
>
> Run the checks required by the phase and report the exact commands and results. Update README and relevant docs. Commit one coherent change for each completed phase using `<type>(<scope>): <subject>`. Do not claim tests passed if they were not run. Do not force-push, rewrite history, expose secrets, or deploy/push externally unless the user has authorized it. If a provider credential blocks a live test, complete mock-backed tests and state the exact remaining step.
>
> End each phase with: what changed; files changed; checks run and results; acceptance criteria status; known limitations; exact commit message; next phase.

### Git workflow

Use the repository's established policy. If the user specifies direct commits to `main`, make a separate verified commit per phase on that branch. Otherwise, use a feature branch and pull request. Do not push or merge unless authorized.

```bash
git status --short
git switch -c feat/phase-NN-short-name
# implement the phase and run the required checks
git add <reviewed-paths>
git commit -m "feat(scope): concise subject"
git push -u origin feat/phase-NN-short-name
```

## 14. Definition of done

- The learner can sign in, set a goal and level, complete a structured lesson, answer by text or speech, receive relevant feedback, retry, and see a justified next activity.
- The product has novice-friendly instruction and a curriculum structure that can expand to more levels and audiences.
- Speaking feedback is task-based, transparent, cautious, and respectful of English varieties.
- Audio consent, access, retention, and deletion are implemented and documented.
- The app is responsive, accessible, tested, documented, and deployable from a clean repository checkout.
- Every phase has a clear commit and a concise explanation of implementation decisions.

## 15. Official technical references

Use current documentation while implementing; check version-specific guidance before selecting dependencies or browser features.

- [Django REST Framework](https://www.django-rest-framework.org/)
- [React: TypeScript](https://react.dev/learn/typescript)
- [MDN: Web Speech API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API)
- [MDN: SpeechRecognition](https://developer.mozilla.org/en-US/docs/Web/API/SpeechRecognition)
- [MDN: MediaStream Recording API](https://developer.mozilla.org/en-US/docs/Web/API/MediaStream_Recording_API)
