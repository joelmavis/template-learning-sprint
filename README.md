# Learning Sprint

## Folder order

- `01-workspace/` — the learner's active and future Sprints.
- `03-templates/` — the clean Sprint starter.
- `04-tools/` — Sprint creation, report generation and validation utilities.
- `05-tests/` — isolated maintainer fixtures; not part of the starting workspace.

Learning Sprint turns a topic, a public course link, or attached study material into a guided learning journey. An agent plans the Sprint, teaches one lesson at a time, reviews your work, records useful knowledge and mistakes, and adjusts what comes next.

## Start in one sentence

Open this folder in puppyone Desktop and tell an agent what you want to learn. For example:

- “Create a 7-day photography plan for a beginner. I have 30 minutes per Session.”
- “Help me study this English course with a 14-day suggested plan: [public URL].”
- “Use the files I attached to create a flexible 30-day data analysis Sprint.”

The agent may ask only the questions needed to set a useful goal, starting level, available time, and source mode. It creates the files, prepares the first lesson, and keeps them updated. You do not need to edit CSV files, move materials, or run scripts.

## The learning loop

Every Sprint follows the same loop:

**Plan → Learn → Practise → Review → Adapt**

A lesson is not complete just because time passed. Your practice must be submitted and reviewed. “Mastered” is used only when the work provides evidence; otherwise the record says developing, needs review, or unassessed.

## Continue later or switch agents

Say “Let’s continue my Learning Sprint.” The agent reads the active Sprint, the latest lesson, progress, mistakes, knowledge notes, and handoff before continuing. A different compatible file-based agent can use those same records; you should not have to explain the history again.

## Three ways to learn

- **Learn a topic:** the agent creates an original course for your goal.
- **Learn from a link:** the agent records what it could actually access, links the source, and never claims to have read blocked or paid material.
- **Learn from files:** attach material in the Agent conversation. The agent records which files it could read and preserves only the material you authorize. Attachment persistence and cross-agent visibility depend on the client; see `QA.md` for the tested boundary.

## Progress and reports

Open `dashboard.html` for a simple overview. Each Sprint has `learning-report.html`, which puts progress, usable knowledge, weak points, and the next step first. Completed Session records remain in the report as expandable details.

The report shows the current practice and a simple answer format. Submit answers in the Agent conversation; the Agent records the actual response, provides feedback, and updates the next Session. The HTML report is a readable record, not a separate form, so the workflow does not depend on preview links or local form storage.

**My Knowledge** is evidence-based. It shows what reviewed practice has demonstrated, what is still developing, and what needs review. Lesson content does not appear there merely because it was displayed or read.

**Day and Session are different.** A Day is the suggested position in a learning plan. A Session is one lesson, practice, and review cycle. You can pause between Sessions, move them to another day, or complete more than one in a day without changing the learning sequence.

If links do not open inside the Desktop HTML preview, use the file path printed beside the link, open that file from the project tree, or ask the agent to open it. Navigation never depends on a clickable link alone.

## Clean starting workspace

The Dashboard starts empty and guides you to create the first Sprint through Agent chat. Real learning records belong in `01-workspace/sprints/` and are ignored by Git by default.

Maintainer regression data lives under `05-tests/fixtures/`. It checks the three source modes, different progress states, and report generation without appearing in the Dashboard or being copied into a learner Sprint.

## Maintainer notes

Agents refresh the dashboard and reports with `python3 04-tools/build_reports.py` and check consistency with `python3 04-tools/validate_workspace.py`. These are not end-user setup steps.

## Two validation modes

- **User Workspace Mode** is the normal learning workflow. `python3 04-tools/validate_workspace.py` accepts populated personal Sprints and checks lesson evidence, reports, mistakes, sources, and links.
- **Template Release Mode** is only for maintainers preparing the blank public template. `python3 04-tools/check_public_release.py` intentionally blocks active Sprints, learner records, and a Dashboard generated from personal work.

Agents must not run Template Release Mode after each lesson and must never delete learner records to make it pass. If this folder still points to GitHub or GitLab, move personal learning work to a private copy before adding submissions or attachments.
