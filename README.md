# Learning Sprint

Learning Sprint turns a topic, a public course link, or attached study material into a guided learning journey. An agent plans the Sprint, teaches one lesson at a time, reviews your work, records useful knowledge and mistakes, and adjusts what comes next.

## Start in one sentence

Open this folder in puppyone Desktop and tell an agent what you want to learn. For example:

- “I want to learn photography basics in seven sessions. I am a beginner and have 30 minutes each time.”
- “Help me study this English course in 14 sessions: [public URL].”
- “Use the files I attached to create a 30-session data analysis Sprint.”

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

Open `dashboard.html` for a simple overview. Each Sprint has `learning-report.html` with what was learned, practice and feedback, review needs, and the next lesson. If links do not open inside the Desktop HTML preview, open the named file from the project tree or ask the agent to open it.

## Examples

`example/` contains three complete, fictional learning records:

- 7-session Photography Basics — complete, created by an agent.
- 14-session Everyday English — 6 sessions complete, based on the accessible scope of public British Council LearnEnglish pages.
- 30-session Data Analysis Fundamentals — 5 sessions complete, using bundled public-safe example files.

Example progress is illustrative and is never copied into a new Sprint. Real learning records belong in `workspace/sprints/` and are ignored by Git by default.

## Maintainer notes

Agents refresh the dashboard and reports with `python3 tools/build_reports.py` and check consistency with `python3 tools/validate_workspace.py`. These are not end-user setup steps.
