#!/usr/bin/env python3
"""Re-run bin/bootcamp verify on recorded stages (path taken from each transcript) and save verify.txt."""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from course_data import PARTS  # noqa: E402

for part in PARTS:
    if len(sys.argv) > 1 and str(part["n"]) not in sys.argv[1:]:
        continue
    ev = ROOT / "parts" / part["slug"] / "evidence" / "recorded-run"
    turn1 = ev / "turn1.jsonl"
    if not turn1.exists():
        continue
    cwd = next((json.loads(l).get("cwd") for l in turn1.read_text().splitlines()
                if '"subtype": "init"' in l or '"subtype":"init"' in l), None)
    summary = json.loads((ev / "summary.json").read_text())
    stage = Path(cwd)
    if summary.get("worktree"):
        stage = Path(cwd)
        if ".claude/worktrees" not in str(stage):
            stage = stage / summary["worktree"]
    if not stage.exists():
        print(f"{part['n']:02d}: stage {stage} missing")
        continue
    (stage / ".bootcamp").mkdir(exist_ok=True)
    (stage / ".bootcamp" / "part").write_text(f"{part['n']:02d}\n")
    proc = subprocess.run([str(ROOT / "bin" / "bootcamp"), "verify", "--dir", str(stage)], capture_output=True, text=True)
    (ev / "verify.txt").write_text(proc.stdout + proc.stderr)
    status = subprocess.run(["git", "status", "--short"], cwd=stage, capture_output=True, text=True).stdout
    (ev / "git-status.txt").write_text("\n".join(l for l in status.splitlines() if ".verify-tasks" not in l and ".bootcamp/" not in l) + "\n")
    print(f"{part['n']:02d}: exit {proc.returncode} · {proc.stdout.count('PASS')} PASS · {proc.stdout.count('FAIL')} FAIL")
