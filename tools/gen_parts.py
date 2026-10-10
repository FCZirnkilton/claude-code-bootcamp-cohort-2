#!/usr/bin/env python3
"""Generate parts/NN/README.md (instructor runbook) and parts/NN/PROMPTS.md from tools/course_data.py."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from course_data import PARTS, schedule  # noqa: E402

SLOTS = {p["n"]: (s, e) for kind, p, s, e, _ in schedule() if kind == "part"}

FALLBACK_NOTES = {
    7: "Claude in Chrome needs the Chrome extension and a claude.ai login. Without it, use `templates/browser-verification-checklist.md` with the captured screenshots in `evidence/`.",
    11: "Agent Teams are experimental (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`). Learners without access review the recorded transcript in `evidence/recorded-run/`, the task board in the checkpoint's `docs/team-plan.md`, and the diff (`bin/bootcamp diff 11`).",
    13: "Cowork needs a paid Claude plan and the Claude desktop app. Without it, run the `stakeholder-update` skill from `skills-pack/` in Claude Code with the same inputs.",
    14: "Remote Control needs a claude.ai login (Team/Enterprise: enabled by an Owner). The demo runs locally; learners without access design the routine with `templates/post-release-routine-brief.md`.",
}


def readme(p: dict) -> str:
    start, end = SLOTS[p["n"]]
    nn = f"{p['n']:02d}"
    lines = [
        f"# Part {nn} · {p['title']}",
        "",
        f"**{p['project']}** · {p['minutes']} minutes · {start}–{end} (brief schedule)",
        "",
        "## Learning goals",
        *[f"- {g}" for g in p["goals"]],
        "",
        "## Learners leave with",
        *[f"- {o}" for o in p["outputs"]],
        "",
        "## Run it",
        "```sh",
        f"# terminal B (this bootcamp repo)",
        f"bin/bootcamp stage {nn}      # fresh Shipyard repo at ~/shipyard-stage + baseline commit",
        "# terminal A",
        "cd ~/shipyard-stage && claude --model sonnet",
        "# ... paste the prompts from PROMPTS.md ...",
        "# terminal B",
        "bin/bootcamp verify           # acceptance checks on ~/shipyard-stage",
        "```",
        "",
        "## Timing inside the part",
        f"- {max(3, p['minutes'] // 6)} min: topic slides",
        f"- {max(2, p['minutes'] // 5)} min: live demo or recorded video (deck)",
        f"- {max(3, p['minutes'] // 4)} min: explain and discuss",
        f"- rest: hands-on lab",
        "",
        "## Lab",
        p["lab"],
        "",
        "## Evidence to show (not claims)",
        *[f"- {e}" for e in p["evidence"]],
        "",
        "## Discussion",
        *[f"- {d}" for d in p["discussion"]],
        "",
        "## If it goes wrong",
        f"- Load the prepared reference: `bin/bootcamp fallback {nn}` (say clearly that it is prepared, not live).",
        f"- Or jump to the full reference state: `bin/bootcamp checkpoint {nn} --force`.",
        f"- Play the recorded run in the deck (video `{nn}`): {p['video']}",
    ]
    if p["n"] in FALLBACK_NOTES:
        lines.append(f"- Availability: {FALLBACK_NOTES[p['n']]}")
    lines += [
        "",
        "## Files",
        "- `start/` — overlay that creates the starting state (briefs, inputs)",
        "- `solution/` — overlay that creates the reference checkpoint",
        "- `evidence/` — captured screenshots, outputs and the recorded Claude Code run (`recorded-run/`)",
        "",
    ]
    return "\n".join(lines)


def prompts(p: dict) -> str:
    lines = [f"# Part {p['n']:02d} prompts", "",
             "Copy each block into Claude Code in order. Read the output before sending the next one.", ""]
    for i, (label, text) in enumerate(p["prompts"], start=1):
        lines += [f"## {i}. {label}", "", "```text", text, "```", ""]
    return "\n".join(lines)


def video_seconds(slug: str) -> str:
    import subprocess
    import shutil
    video = ROOT / "videos" / f"{slug}.mp4"
    if not video.exists() or not shutil.which("ffprobe"):
        return "–"
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(video)],
                         capture_output=True, text=True).stdout.strip()
    return f"{float(out):.0f} s" if out else "–"


def run_of_show() -> str:
    lines = ["# Run of show", "",
             "Generated from `tools/course_data.py` by `tools/gen_parts.py`. Times follow the brief's schedule table; "
             "shift them if the cohort starts at 10:00 ET.", "",
             "| Time | Block | Min | Video | Fallback |", "|---|---|--:|--:|---|"]
    for kind, b, start, end, minutes in schedule():
        if kind == "part":
            lines.append(f"| {start}–{end} | **Part {b['n']:02d}** · {b['title']} ({b['project'].split(':')[0]}) | {minutes} | "
                         f"{video_seconds(b['slug'])} | `bin/bootcamp fallback {b['n']:02d}` |")
        elif kind == "break":
            lines.append(f"| {start}–{end} | {b} | {minutes} | | catch up: `bin/bootcamp checkpoint NN --force` |")
        else:
            lines.append(f"| {start}–{end} | {b} | {minutes} | | |")
    lines += ["", "## Inside every part", "",
              "1. Section slide → goals → concept slides (≈ 1/6 of the slot)",
              "2. Prompt slide(s): the exact prompt, read aloud",
              "3. Video slide: click to play the recorded real run (≈ 1–2 min); pause for questions",
              "4. Evidence slide: what the run proved",
              "5. Discussion slide (≈ 1/4 of the slot)",
              "6. Lab slide: learners stage the part and run the prompts; checkpoint slide to close", ""]
    return "\n".join(lines)


def main() -> None:
    for p in PARTS:
        d = ROOT / "parts" / p["slug"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "README.md").write_text(readme(p))
        (d / "PROMPTS.md").write_text(prompts(p))
    (ROOT / "docs" / "RUN-OF-SHOW.md").write_text(run_of_show())
    print(f"wrote README.md and PROMPTS.md for {len(PARTS)} parts, and docs/RUN-OF-SHOW.md")


if __name__ == "__main__":
    main()
