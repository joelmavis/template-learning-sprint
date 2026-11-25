# Daily Learning

> **Turn any learning goal or local study material into a guided, evidence-based learning sprint — all inside one local workspace.**

[![License: MIT](https://img.shields.io/badge/License-MIT-1f7a63.svg)](./LICENSE)
[![Offline First](https://img.shields.io/badge/Reports-Single--File%20Offline-2e9e7e)](#)

Daily Learning turns a learning goal or local study material into a structured learning journey. An AI Agent plans your Sprint, teaches one lesson at a time, reviews your submitted practice, tracks real mastery and mistakes, and adapts what comes next.

---

## Quickstart Guide (3 Simple Steps)

You never need to create folders, hand-edit CSV files, or run scripts manually—the Agent manages everything for you.

### Step 1: Get This Template
- **Option A (Recommended in Puppyone):** Click **"Use this template" (使用此模版)** on the Puppyone template details page to create a workspace immediately.
- **Option B (Git Clone):** Clone this repository locally and open the folder:
  ```bash
  git clone https://github.com/joelmavis/template-learning-sprint.git
  cd template-learning-sprint
  ```

### Step 2: Preview Your Dashboard Directly
In the left file tree, click **`dashboard.html`** to open the built-in HTML preview (no external browser or local server required). Once a Sprint starts, each Sprint also generates an interactive **`learning-report.html`** with mastery charts, 1-click answer templates, and a sortable/draggable mistake review table.

### Step 3: Start Learning in One Sentence
Open the **Agent Chat** panel and copy-paste one of the 4 starter prompts below (or attach your own local notes/PDFs/slides):

1. **Language Learning:**
   ```text
   Create a 7-day Business English writing Sprint for clearer work emails and meeting summaries. I have 25 minutes per Session.
   ```
2. **LLM Fundamentals:**
   ```text
   Create a 10-day LLM fundamentals Sprint covering tokens, embeddings, RAG, and agent workflows for a beginner. I have 30 minutes per Session.
   ```
3. **Finance Basics:**
   ```text
   Create a 7-day Finance fundamentals Sprint covering financial statements, cash flow, and risk basics. I have 25 minutes per Session.
   ```
4. **Generate Theme & Plan from Local Files:**
   ```text
   Use the local notes and PDFs I attached to identify key themes and create a flexible 14-day learning Sprint with daily recall practice.
   ```

The Agent asks only the minimal questions needed to clarify your goal, level, and available time, creates the Sprint files, prepares Lesson 1, and refreshes `dashboard.html`.

---

## Common Agent Prompts Cheat Sheet

| Goal | Where to Input | Prompt to Copy & Send |
| :--- | :--- | :--- |
| **Start a new course** | Agent Chat | `Create a 7-day <topic> plan for a beginner. I have 30 minutes per Session.` |
| **Learn from local files** | Agent Chat | `Use the local files I attached to create a flexible learning Sprint.` |
| **Continue where you left off** | Agent Chat | `Let’s continue Daily Learning.` |
| **Submit practice answers** | Agent Chat | Click **Copy Answer Template** in `learning-report.html`, fill in your answers, and paste into Agent chat |
| **Focus on weak points** | Agent Chat | `Review my unresolved mistakes and give me a short retrieval practice before the next lesson.` |
| **Switch or adjust goal** | Agent Chat | `Adjust my remaining lessons to focus more on <subtopic> while keeping completed progress.` |

---

## The Learning Loop & Evidence Rules

Every Sprint follows the same 5-step loop:

**Plan → Learn → Practise → Review → Adapt**

- **Evidence over passive reading:** A lesson is never marked `completed` just because time passed or you read it—your practice must be submitted and reviewed in Agent chat.
- **Honest mastery tracking:** **My Knowledge** shows only what reviewed practice has demonstrated (`Demonstrated`, `Still Developing`, `Needs Review`).
- **Day vs. Session:** A **Day** is the suggested sequence in your plan; a **Session** is one complete lesson + practice + review cycle. You can pause between Sessions or finish multiple Sessions in one day.
- **Seamless Agent handoff:** Say **“Let’s continue Daily Learning.”** anytime—even after switching Agents—and it resumes from your actual files and `handoff.md`.
- **Local-first source modes:** Supports `agent_generated` courses and `attached_files` (readable local files). Pasting a URL is not a separate ingestion mode.

---

## Folder Structure

- `dashboard.html` — Top-level interactive overview (preview directly in built-in HTML view).
- `01-workspace/` — Your active and future Sprints (ignored by Git by default).
- `03-templates/` — Clean Sprint starter scaffold.
- `04-tools/` — Sprint creation, report generation (`build_reports.py`), and validation utilities.
- `05-tests/` — Disposable-workspace smoke test (`smoke_test.py`); contains no committed sample courses.

---

## Maintainer Notes & Validation Modes

Agents automatically refresh reports with `python3 04-tools/build_reports.py` and verify workspace consistency with `python3 04-tools/validate_workspace.py`.

- **User Workspace Mode:** `python3 04-tools/validate_workspace.py` accepts populated personal Sprints and checks lesson evidence, reports, mistakes, sources, and links.
- **Template Release Mode:** `python3 04-tools/check_public_release.py` is reserved for maintainers preparing a blank public template and intentionally blocks active Sprints or personal learner records.
