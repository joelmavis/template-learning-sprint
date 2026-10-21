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

print("PASSED disposable workflow smoke test; no test Sprint was retained.")
