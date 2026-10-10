#!/usr/bin/env python3
"""Record a real headless Claude Code run of one workshop part.

Stages the part's starting repo, sends the part's prompts from course_data.py (multi-turn via --resume),
saves raw stream-json transcripts, then runs the acceptance checks. The transcripts feed the deck videos.

    tools/record_run.py 05 [--out ~/bootcamp-recordings] [--model sonnet]
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from course_data import PARTS  # noqa: E402

ALLOWED = ("Read Edit Write Glob Grep Agent Skill TodoWrite "
           "Bash(python3 *) Bash(node *) Bash(git status *) Bash(git diff *) Bash(git log *) "
           "Bash(git worktree list *) Bash(ls *) Bash(cat *) Bash(head *) Bash(tail *) Bash(wc *) "
           "Bash(grep *) Bash(curl -s *) Bash(sleep *) Bash(kill *) Bash(mkdir *) Bash(claude plugin validate *)")

# Per part and per turn: permission mode and extra CLI flags. Default: acceptEdits, no flags.
TURN_OPTIONS: dict[int, list[dict]] = {
    3: [{}, {"before": [("Human approves the rules (headless runs cannot approve edits under .claude/): install the reference rules",
                         "mkdir -p .claude/rules && cp {root}/parts/03-project-brain/solution/.claude/rules/*.md .claude/rules/ && head -4 .claude/rules/*.md")]}],
    2: [{"mode": "plan"}, {}],
    4: [{"mode": "plan"}, {}],
    6: [{"flags": ["--worktree", "search-tags"]}],
    9: [{}, {"before": [("Lab step: the human wires the hooks into .claude/settings.json (PreToolUse + PostToolUse)",
                         "cp {root}/parts/09-quality-pack/solution/.claude/settings.json .claude/settings.json && grep -o 'block-unsafe-commands.sh\\|post-edit-validate.sh' .claude/settings.json")]}],
    7: [{}],                                   # Chrome turn is recorded with captured browser evidence instead
    8: [{"mode": "plan"}, {}],
    10: [{}, {"flags": ["--plugin-dir", "./plugins/engineering-quality"]}],
    11: [{"env": {"CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"}},
         {"env": {"CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"}}],
}


def run_turn(cwd: Path, prompt: str, out: Path, model: str, session: str | None, opts: dict) -> dict:
    cmd = ["claude", "-p", prompt, "--model", model, "--output-format", "stream-json", "--verbose",
           "--permission-mode", opts.get("mode", "acceptEdits"), "--allowedTools", ALLOWED + " " + opts.get("extra_allowed", ""),
           "--max-budget-usd", "4", "--include-hook-events"]
    if session:
        cmd += ["--resume", session]
    cmd += opts.get("flags", [])
    env = {**os.environ, **opts.get("env", {}), "SHIPCTL_DB": str(cwd / "tasks.json")}
    started = time.time()
    with out.open("w") as fh:
        proc = subprocess.run(cmd, cwd=cwd, stdout=fh, stderr=subprocess.PIPE, text=True, env=env, timeout=1800)
    result = {"exit": proc.returncode, "seconds": round(time.time() - started), "stderr": proc.stderr[-2000:]}
    for line in out.read_text().splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "system" and event.get("subtype") == "init":
            result["session_id"] = event.get("session_id")
        if event.get("type") == "result":
            result.update(cost_usd=event.get("total_cost_usd"), turns=event.get("num_turns"),
                          duration_ms=event.get("duration_ms"), result_subtype=event.get("subtype"))
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("part", type=int)
    parser.add_argument("--out", default=str(Path.home() / "bootcamp-recordings"))
    parser.add_argument("--model", default="sonnet")
    parser.add_argument("--isolate", metavar="DIR", help="stage in a fresh unique directory under DIR (no sibling runs visible)")
    args = parser.parse_args()
    part = next(p for p in PARTS if p["n"] == args.part)
    import tempfile
    stage = Path(tempfile.mkdtemp(prefix=f"shipyard-{args.part:02d}-", dir=args.isolate)) / "shipyard" if args.isolate else Path(args.out).expanduser() / f"{args.part:02d}"
    subprocess.run([str(ROOT / "bin" / "bootcamp"), "stage", str(args.part), "--dir", str(stage), "--force"], check=True)
    evidence = ROOT / "parts" / part["slug"] / "evidence" / "recorded-run"
    evidence.mkdir(parents=True, exist_ok=True)
    options = TURN_OPTIONS.get(args.part, [{}] * len(part["prompts"]))
    session, summary = None, {"part": args.part, "model": args.model, "turns": []}
    for i, ((label, prompt), opts) in enumerate(zip(part["prompts"], options), start=1):
        print(f"[part {args.part:02d}] turn {i}: {label}", flush=True)
        human = []
        for desc, command in opts.get("before", []):
            command = command.replace("{root}", str(ROOT))
            proc = subprocess.run(["bash", "-c", command], cwd=stage, capture_output=True, text=True)
            human.append({"description": desc, "command": command.replace(str(ROOT), "<bootcamp>"),
                          "output": (proc.stdout + proc.stderr)[-1500:], "exit": proc.returncode})
        result = run_turn(stage, prompt, evidence / f"turn{i}.jsonl", args.model, session, opts)
        session = result.get("session_id") or session
        summary["turns"].append({"label": label, "prompt": prompt, "options": {k: v for k, v in opts.items() if k != "before"},
                                 "human_steps": human, **result})
        print(f"   exit={result['exit']} {result['seconds']}s cost=${result.get('cost_usd')}", flush=True)
        if result["exit"] != 0:
            break
    work = stage
    if args.part == 6:
        worktrees = sorted((stage / ".claude" / "worktrees").glob("*"))
        work = worktrees[0] if worktrees else stage
        summary["worktree"] = str(work.relative_to(stage)) if worktrees else None
    for name, cmd in [("git-status", ["git", "status", "--short"]),
                      ("git-diff-stat", ["git", "diff", "--stat"]),
                      ("verify", [str(ROOT / "bin" / "bootcamp"), "verify", "--dir", str(work)])]:
        proc = subprocess.run(cmd, cwd=work, capture_output=True, text=True)
        (evidence / f"{name}.txt").write_text(proc.stdout + proc.stderr)
        summary[name] = proc.returncode
    (evidence / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({k: v for k, v in summary.items() if k != "turns"}), flush=True)


if __name__ == "__main__":
    main()
