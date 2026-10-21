# Learning Sprint v1.0 — QA

Status meanings: **Passed** means verified in this local Work environment; **Partially Tested** means only part of the path was exercised; **Not Tested** means no claim is made.

| Check | Status | Evidence / limitation |
|---|---|---|
| File structure and schema | Passed | `python3 04-tools/validate_workspace.py` checked required files, CSV columns, stable lesson references, mistake evidence, reports, and links on 2026-10-20. |
| Report generation | Passed | `python3 04-tools/build_reports.py` regenerated the clean-start Dashboard. The disposable smoke test also generated an active Sprint report without committing its records. |
| Temporary workflow smoke test | Passed | `python3 05-tests/smoke_test.py` creates a temporary Sprint, verifies answer guidance and My Knowledge boundaries, passes daily validation, confirms release mode blocks the populated copy, and deletes the temporary directory automatically. |
| Public-link source boundary | Partially Tested | Source-access boundaries remain enforced by Agent rules and `sources.md`; no public-link course is committed as test data. A fresh external-link UAT is still required for current access behavior. |
| Attached-file learning path | Partially Tested | A private AI Governance Word-file UAT created a seven-Session Sprint, source record, first lesson, practice and report. Cross-client attachment persistence remains untested. |
| Natural-language zero-config start | Partially Tested | In a temporary copy, the Agent-facing creator produced a five-lesson Sprint, active pointer, report, and Dashboard without manual file setup. The natural-language path in puppyone Desktop remains untested. |
| Conversation attachment persistence | Not Tested | Must be tested in puppyone Desktop with a real attachment and a second Agent. |
| Cross-Agent continuation | Partially Tested | A second Work Agent located the active Sprint from files alone, reviewed the recorded L01 submission, updated progress/mistakes/knowledge/handoff, adapted L02, and refreshed the report. Claude Code and a second puppyone Agent remain untested. |
| Normal-browser HTML | Passed | The clean-start Dashboard and private UAT report render with the existing visual system. Completed Session records remain collapsed by default, and static validation checks all local links. |
| puppyone Desktop rendering and navigation | Not Tested | Known prior evidence suggests HTML preview links may not navigate. Every important destination now also shows its project-relative file path, so the user can open it from the tree or ask an Agent. |
| puppyone preview icon | Source Checked | The generated HTML contains no dog icon and no fixed-position element. Any fixed dog icon shown at the right edge belongs to the client preview UI and cannot be repositioned by this template. |
| Non-developer usability | Not Tested | Requires an independent person using only README and Agent chat. |
| Privacy and public safety | Passed | Local scan found no credentials, private keys, absolute developer paths, oversized files, real learner records, committed test courses, or prohibited template-brand marketing phrases. |

Do not upgrade a status without recording the environment and observable result.

Daily validation is User Workspace Mode and is expected to pass with active learner data. Public-release safety is checked separately with `python3 04-tools/check_public_release.py` in a clean release copy. The release checker should reject a populated learner workspace; no Agent or automated test may remove learner records to make it pass.

**Mode-separation regression — 2026-10-21:** In a disposable copy, a complete active Sprint was added under `01-workspace/sprints/`. Report generation produced a personal report without the sample footer; daily validation passed with the active Sprint intact. Template Release Mode blocked the active pointer, and the learner's progress data remained present.

## Cross-Agent handoff test

Tested in a temporary copy on 2026-10-20:

1. The first Agent created a five-lesson `Decision Writing` Sprint and recorded an L01 learner submission.
2. A second Agent was told only the temporary workspace path. It followed `AGENTS.md`, resolved `01-workspace/active-sprint.txt`, and read the latest Sprint handoff.
3. It marked L01 `completed / reviewed / emerging`, explained why three informal reactions did not support a full rollout, and identified the one-sided trade-off.
4. It created M001 and M002, updated `knowledge.md`, prepared L02 around evidence calibration, advanced the active lesson, regenerated HTML, and passed validation.

No additional learner submission was invented. The temporary workflow test did not modify the public workspace or add committed test data.

**Clean-start and name-first regression — 2026-10-21:** The Dashboard contains no preloaded Sprint and shows a first-Sprint prompt. Lesson titles, knowledge-point names, and mistake concepts precede optional internal IDs in generated reports. The former learning samples are no longer included in the public repository; workflow checks run in a disposable temporary copy.
