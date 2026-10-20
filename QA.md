# Learning Sprint v1.0 — QA

Status meanings: **Passed** means verified in this local Work environment; **Partially Tested** means only part of the path was exercised; **Not Tested** means no claim is made.

| Check | Status | Evidence / limitation |
|---|---|---|
| File structure and schema | Passed | `python3 tools/validate_workspace.py` checked required files, CSV columns, stable lesson references, mistake evidence, reports, and links on 2026-10-20. |
| Report generation | Passed | `python3 tools/build_reports.py` regenerated three example reports and `dashboard.html`. |
| Example consistency | Passed | Validator confirmed Photography 7/7, English 6/14, and Data Analysis 5/30; every completed lesson has learning content, practice, a submission, feedback, and adaptation. |
| Public-link source boundary | Passed | British Council LearnEnglish public pages were accessible on 2026-10-20; only page scope and topic descriptions are used. Lessons and practice are original. |
| Bundled-file learning path | Passed | The data-analysis example uses original `materials/course-notes.md` and `practice-data.csv`; the first five reviewed lessons are consistent with those files. This does not prove conversation-upload persistence. |
| Natural-language zero-config start | Partially Tested | In a temporary copy, the Agent-facing creator produced a five-lesson Sprint, active pointer, report, and Dashboard without manual file setup. The natural-language path in puppyone Desktop remains untested. |
| Conversation attachment persistence | Not Tested | Must be tested in puppyone Desktop with a real attachment and a second Agent. |
| Cross-Agent continuation | Partially Tested | A second Work Agent located the active Sprint from files alone, reviewed the recorded L01 submission, updated progress/mistakes/knowledge/handoff, adapted L02, and refreshed the report. Claude Code and a second puppyone Agent remain untested. |
| Normal-browser HTML | Passed | Dashboard and Photography report rendered in the in-app browser; clicking the relative report link opened the correct report. Static validation checked all local links. |
| puppyone Desktop rendering and navigation | Not Tested | Known prior evidence suggests HTML preview links may not navigate. The workflow provides project-tree and Agent alternatives. |
| Non-developer usability | Not Tested | Requires an independent person using only README and Agent chat. |
| Privacy and public safety | Passed | Local scan found no credentials, private keys, absolute developer paths, oversized files, real learner records, or prohibited template-brand marketing phrases. Bundled data is fictional and public-safe. |

Do not upgrade a status without recording the environment and observable result.

## Cross-Agent handoff test

Tested in a temporary copy on 2026-10-20:

1. The first Agent created a five-lesson `Decision Writing` Sprint and recorded an L01 learner submission.
2. A second Agent was told only the temporary workspace path. It followed `AGENTS.md`, resolved `workspace/active-sprint.txt`, and read the latest Sprint handoff.
3. It marked L01 `completed / reviewed / emerging`, explained why three informal reactions did not support a full rollout, and identified the one-sided trade-off.
4. It created M001 and M002, updated `knowledge.md`, prepared L02 around evidence calibration, advanced the active lesson, regenerated HTML, and passed validation.

No additional learner submission was invented. The temporary fixture is not included in the deliverable and did not modify the public examples.
