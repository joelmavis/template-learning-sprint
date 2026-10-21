#!/usr/bin/env python3
"""Exercise the learning workflow in a disposable copy without committed fixtures."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def run(*args, cwd, expect=0):
    result = subprocess.run([sys.executable, *args], cwd=cwd, capture_output=True, text=True)
    if result.returncode != expect:
        print(result.stdout, end="")
        print(result.stderr, end="", file=sys.stderr)
        raise SystemExit(f"Unexpected exit {result.returncode}: {' '.join(args)}")
    return result


with tempfile.TemporaryDirectory(prefix="learning-sprint-test-") as temporary:
    copy = Path(temporary) / "workspace"
    shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns(".git", "__pycache__", ".DS_Store"))
    rejected = run(
        "04-tools/create_sprint.py",
        "--title", "Unsupported URL Sprint",
        "--goal", "Confirm URL ingestion is not a supported starting mode.",
        "--mode", "public_link",
        "--lessons", "1",
        cwd=copy,
        expect=2,
    )
    if "invalid choice" not in rejected.stderr or (copy / "01-workspace/sprints/unsupported-url-sprint").exists():
        raise SystemExit("URL ingestion was not rejected cleanly")
    run(
        "04-tools/create_sprint.py",
        "--title", "Temporary Test Sprint",
        "--goal", "Verify the local learning workflow without publishing test data.",
        "--mode", "agent_generated",
        "--lessons", "2",
        "--minutes", "15",
        "--level", "Beginner",
        "--slug", "temporary-test-sprint",
        cwd=copy,
    )
    run("04-tools/validate_workspace.py", cwd=copy)
    release = run("04-tools/check_public_release.py", cwd=copy, expect=1)
    if "Public template contains an active Sprint pointer" not in release.stderr:
        raise SystemExit("Release Mode did not explain why the populated copy was blocked")
    report = copy / "01-workspace/sprints/temporary-test-sprint/learning-report.html"
    text = report.read_text(encoding="utf-8")
    for phrase in ("Practice task", "Submit in Agent chat", "My Knowledge reflects reviewed learner evidence"):
        if phrase not in text:
            raise SystemExit(f"Generated report lacks: {phrase}")

    dashboard = (copy / "dashboard.html").read_text(encoding="utf-8")
    if "<h1>Daily Learning</h1>" not in dashboard or "<title>Daily Learning</title>" not in dashboard:
        raise SystemExit("Dashboard does not use the Daily Learning product name")
    if "public course link" in dashboard or "Public link" in dashboard:
        raise SystemExit("Dashboard still offers URL ingestion")

print("PASSED disposable workflow smoke test; no test Sprint was retained.")
