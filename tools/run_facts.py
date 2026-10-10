"""Extract verifiable facts from a recorded run (parts/NN/evidence/recorded-run/)."""

from __future__ import annotations

import json
import re
from pathlib import Path

ANSI = re.compile(r"\x1b\[[0-9;]*m")
TEST_LINE = re.compile(r"(Ran \d+ tests?[^\n]*|# pass \d+|# fail \d+|^OK$|FAILED \([^)]*\))", re.M)


def facts(evidence: Path) -> dict:
    summary = json.loads((evidence / "summary.json").read_text())
    tools, test_lines = 0, []
    for turn_file in sorted(evidence.glob("turn*.jsonl")):
        for line in turn_file.read_text().splitlines():
            try:
                e = json.loads(line)
            except json.JSONDecodeError:
                continue
            msg = e.get("message")
            content = msg.get("content") if isinstance(msg, dict) else None
            if e.get("type") == "assistant" and isinstance(content, list):
                tools += sum(1 for b in content if b.get("type") == "tool_use")
            if e.get("type") == "user" and isinstance(content, list):
                for b in content:
                    if b.get("type") == "tool_result":
                        text = b["content"] if isinstance(b["content"], str) else json.dumps(b["content"])
                        found = [m.group(0) for m in TEST_LINE.finditer(text.replace("\\n", "\n"))]
                        if any(f.startswith(("Ran", "# pass")) for f in found):
                            test_lines = [f for f in found if f.startswith(("Ran", "# pass", "FAILED"))]
    verify = ANSI.sub("", (evidence / "verify.txt").read_text()) if (evidence / "verify.txt").exists() else ""
    status = (evidence / "git-status.txt").read_text().split("\n") if (evidence / "git-status.txt").exists() else []
    return {
        "turns": len(summary["turns"]),
        "seconds": sum(t.get("seconds", 0) for t in summary["turns"]),
        "cost": sum(t.get("cost_usd") or 0 for t in summary["turns"]),
        "tool_calls": tools,
        "tests": test_lines[-2:],
        "verify_pass": verify.count("PASS"),
        "verify_fail": verify.count("FAIL"),
        "fail_names": [l.split("FAIL", 1)[1].strip() for l in verify.splitlines() if "FAIL" in l],
        "changed": [l for l in status if l.strip() and ".verify-tasks" not in l],
    }
