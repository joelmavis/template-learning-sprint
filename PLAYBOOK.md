# Learning Sprint Playbook

## 1. Plan

**Trigger:** The user names a topic, provides a public course URL, or uploads learning material.

Confirm only the goal, starting level, available time, approximate sessions, and source mode that are not already clear. Create the Sprint and write `learning-plan.md`, `sources.md`, lesson rows in `progress.csv`, empty mistake and knowledge records, and a first complete lesson.

**Complete when:** the plan is actionable, the source boundary is honest, and the first lesson is ready.

## 2. Learn

Teach the current lesson directly in the conversation and preserve the complete explanation in its lesson Markdown. Distinguish source-derived material from the Agent's explanation. Keep the lesson small enough for the user's stated session length.

**Complete when:** the learner has received the explanation and can attempt the practice.

## 3. Practise

Ask for an observable response: answer, explanation, corrected sentence, calculation, or uploaded work. Record the actual submission under `## Learner submission`. If nothing was submitted, keep the practice open.

**Complete when:** a real submission exists in the Sprint record.

## 4. Review

Explain what was correct, what needs work, and why. Create or update mistake records. Do not equate “read” or “submitted” with mastery.

**Complete when:** feedback is specific and linked to the submitted work.

## 5. Adapt

Update `progress.csv`, `mistakes.csv`, `knowledge.md`, the next lesson, `handoff.md`, and the HTML report. Revisit a weak concept before increasing difficulty.

**Complete when:** another Agent can identify the next action from files alone.

## Recovery rules

- **Link unavailable:** record the failed access and ask for an accessible page, outline, or attached material. Offer an original course only with the user's agreement.
- **Attachment unreadable or not persistent:** say what failed. Ask the user to reattach it or authorize a readable extract to be saved in the Sprint. Do not imply another Agent can see it until verified.
- **No practice submitted:** leave the lesson in progress and resume at practice next time.
- **Long break:** resume the earliest incomplete step; use a short retrieval check before new material.
- **Goal changed:** preserve completed evidence, update the plan and future rows, and record the decision in `handoff.md`.
- **Needs review:** schedule retrieval or a corrective task; update mastery only after new evidence.
- **Agent changed:** read the active pointer and handoff, verify latest CSV state, then continue without asking the learner to manage files.

## Report language

Reports must show the actual goal, source mode, progress, knowledge, representative practice, feedback, unresolved mistakes, and next step. They must be independently readable and must not replace substance with “see file.” Lead with course, lesson, knowledge-point, and mistake names; keep stable IDs secondary.

## Validation modes

During normal learning, regenerate reports and run `python3 04-tools/validate_workspace.py`. This daily check accepts active, partially completed, and completed personal Sprints.

`python3 04-tools/check_public_release.py` is reserved for maintainers preparing a blank public template. Run it from a clean release copy, not after each lesson. A release failure must never be resolved by deleting learner submissions, feedback, mistakes, knowledge, or handoff history.
