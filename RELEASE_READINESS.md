# Daily Learning v1.0 — Release Readiness

## Package status

The package is ready for a public repository update.

- Suggested repository: `template-learning-sprint`
- Suggested license: MIT (included)
- Product name: Daily Learning
- Main workflow: Plan → Learn → Practise → Review → Adapt
- Input modes: Agent-generated course and local files or attachments
- Starting state: empty learner workspace with a guided first-Sprint prompt

## Verified locally

- Required Markdown, CSV, HTML, source, and handoff files are present.
- The clean-start Dashboard regenerates without third-party packages, and no sample courses or test learner records are committed.
- A disposable smoke test creates an active Sprint, checks report and validation behavior, confirms release mode blocks populated learner data, and removes the temporary copy afterward.
- A five-lesson Sprint can be created in a clean copy without manual file setup.
- A second Work Agent continued from shared files, reviewed a submission, updated the learning record, adapted the next lesson, and regenerated the report.
- Dashboard and report render in a normal browser, and the relative report link works.
- Static privacy, credential, developer-path, stale-brand, file-size, source, and link checks pass.
- Daily User Workspace Mode and maintainer-only Template Release Mode are separate; release checks do not require clearing a user's active Sprint.
- Generated HTML leads with course, lesson, knowledge-point, and mistake names; stable IDs remain secondary.

## Open product UAT

- Natural-language creation inside puppyone Desktop.
- Conversation attachment persistence and visibility to a second Agent.
- Claude Code handoff using the same Sprint.
- puppyone Desktop HTML rendering and navigation behavior.
- Independent non-developer usability test.

These items remain explicit in `QA.md`; the package does not claim they passed.
