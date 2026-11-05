# Contributing

Read the README, master plan, and phase record before changing code. Preserve existing user work. Keep each phase a coherent, tested change with documentation and a conventional commit: `type(scope): subject`.

This delivery follows the owner's instruction to commit and push each verified phase to `main`. Fetch first, check divergence, and use fast-forward pushes only. Never force-push or rewrite published history. Other contributors should use pull requests unless the owner authorizes direct delivery.

Use four-space Python indentation, two-space TypeScript indentation, descriptive names, strict TypeScript, small domain-focused modules, and accessible semantic HTML. Automated lint/format configuration follows in Phase 05. Avoid speculative abstractions and dependencies without a concrete need; document licenses and operating costs for new services.

Tests should exercise behavior: permissions and ownership, lesson state transitions, scoring evidence, consent and retention, provider failures, and accessible typed fallbacks. Run phase-specific checks and report exact outcomes, including skips and missing coverage. Do not equate zero collected tests with success. Never weaken validation to pass a gate.

Use synthetic content only. Do not put API keys, real learner data, or voice recordings in commits. Keep providers replaceable; mock results must be visibly distinguished from real evaluation. Any scoring quality or educational-review claim requires actual review evidence.

Before committing: inspect `git diff --check`, review the staged diff and file list, run appropriate checks, update docs/phases.md, and verify no generated dependencies or local environment files are staged. No production deployment or paid service provisioning is implied by a code contribution.
