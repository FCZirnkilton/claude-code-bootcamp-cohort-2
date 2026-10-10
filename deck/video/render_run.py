#!/usr/bin/env python3
"""Render a recorded Claude Code run (parts/NN/evidence/recorded-run/turn*.jsonl) as a large-font MP4.

Everything shown comes from the transcript or from files captured after the run (verify.txt, git-status.txt).
Long runs are condensed (first and last tool calls of each turn); nothing is invented.

    python3 deck/video/render_run.py 05      # → videos/05-resilient-notes.mp4
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
from course_data import PARTS  # noqa: E402

W, H, FPS = 1920, 1080, 12
F = "/usr/share/fonts/truetype/dejavu/"
MONO = ImageFont.truetype(F + "DejaVuSansMono.ttf", 34)
MONOB = ImageFont.truetype(F + "DejaVuSansMono-Bold.ttf", 34)
SANS = ImageFont.truetype(F + "DejaVuSans.ttf", 40)
SMALL = ImageFont.truetype(F + "DejaVuSans-Bold.ttf", 26)
BIG = ImageFont.truetype(F + "DejaVuSans-Bold.ttf", 80)
MID = ImageFont.truetype(F + "DejaVuSans.ttf", 42)

BG, PANEL, BAR = "#060e18", "#0b1626", "#1a283b"
LIME, TXT, MUTED = "#baff70", "#e5e7eb", "#94a3b8"
GREEN, RED, YEL, CYAN = "#4ade80", "#f87171", "#fbbf24", "#67e8f9"
LH, X0, Y0, Y1 = 47, 70, 116, 888
ROWS = (Y1 - Y0) // LH
COLS = 86
SLOW = 1.3
ANSI = re.compile(r"\x1b\[[0-9;]*m")
CARD_NOTES = {
    7: "Chrome step not possible headless: browser evidence was captured separately (Part 7 evidence)",
    11: "Headless run with the Agent Teams flag: the lead runs parallel background agents. Interactive team UI = live demo",
    13: "Cowork fallback path: the same prompt in Claude Code (Cowork itself runs in the desktop app)",
    14: "Remote Control needs an interactive session: this is the same prompt run headless",
}


class Movie:
    def __init__(self, out: Path, chapter: str, tag: str) -> None:
        self.chapter, self.tag = chapter, tag
        self.lines: list[tuple[str, str, bool]] = []
        self.caption, self.term, self.seconds = "", "", 0.0
        self.ff = subprocess.Popen(
            ["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
             "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-threads", "2",
             "-tune", "stillimage", "-crf", "21", "-pix_fmt", "yuv420p", "-profile:v", "high", "-level", "4.0",
             "-movflags", "+faststart", str(out)], stdin=subprocess.PIPE)
        self.frame = b""

    def draw(self) -> None:
        im = Image.new("RGB", (W, H), BG)
        d = ImageDraw.Draw(im)
        d.rounded_rectangle((40, 22, W - 40, 900), 14, fill=PANEL, outline="#22324a", width=2)
        d.rectangle((42, 24, W - 42, 90), fill="#14213a")
        for k, c in enumerate(("#f87171", "#fbbf24", "#4ade80")):
            d.ellipse((66 + k * 34, 46, 88 + k * 34, 68), fill=c)
        d.text((190, 40), self.term, font=SMALL, fill=MUTED)
        d.text((W - 70 - d.textlength(self.tag, font=SMALL), 40), self.tag, font=SMALL, fill=YEL)
        for k, (t, c, b) in enumerate(self.lines[-ROWS:]):
            d.text((X0, Y0 + k * LH), t, font=MONOB if b else MONO, fill=c)
        d.rectangle((0, 918, W, H), fill=BAR)
        d.rectangle((0, 918, 14, H), fill=LIME)
        d.text((50, 930), self.chapter, font=SMALL, fill=LIME)
        for k, t in enumerate(textwrap.wrap(self.caption, 80)[:2]):
            d.text((50, 968 + k * 50), t, font=SANS, fill="white")
        self.frame = im.tobytes()

    def hold(self, sec: float) -> None:
        if sec > 0.1:
            sec *= SLOW
        self.draw()
        for _ in range(max(1, round(sec * FPS))):
            self.ff.stdin.write(self.frame)
        self.seconds += sec

    def add(self, text: str, color: str = TXT, bold: bool = False, indent: int = 0) -> None:
        for raw in text.split("\n"):
            for part in textwrap.wrap(raw, COLS - indent, drop_whitespace=False) or [""]:
                self.lines.append((" " * indent + part, color, bold))

    def para(self, text: str, color: str = TXT, per: float = 0.3, indent: int = 2, limit: int = 99) -> None:
        shown = 0
        for line in text.splitlines():
            for chunk in textwrap.wrap(line, COLS - indent) or [""]:
                if shown >= limit:
                    return
                self.add(" " * indent + chunk, color)
                self.hold(per)
                shown += 1

    def typed(self, prefix: str, text: str, color: str = TXT, cps: int = 150) -> None:
        rows = [w for row in text.split("\n") for w in (textwrap.wrap(row, COLS - len(prefix)) or [""])]
        step = max(1, round(cps / FPS))
        for n, row in enumerate(rows):
            lead = prefix if n == 0 else " " * len(prefix)
            self.lines.append((lead, color, False))
            for i in range(0, len(row) + step, step):
                self.lines[-1] = (lead + row[:i], color, False)
                self.hold(1 / FPS)
        self.hold(0.5)

    def card(self, title: str, sub: str, foot: str, sec: float) -> None:
        im = Image.new("RGB", (W, H), "#101827")
        d = ImageDraw.Draw(im)
        d.text((140, 120), "CLAUDE CODE BOOTCAMP · COHORT 2", font=SMALL, fill=LIME)
        y = 300
        for t in title.split("\n"):
            words, line = t.split(), ""
            for w_ in words:
                if line and d.textlength(line + " " + w_, font=BIG) > W - 280:
                    d.text((140, y), line, font=BIG, fill="white")
                    y, line = y + 100, w_
                else:
                    line = (line + " " + w_).strip()
            d.text((140, y), line, font=BIG, fill="white")
            y += 100
        y += 30
        for t in sub.split("\n"):
            for w_ in textwrap.wrap(t, 68):
                d.text((140, y), w_, font=MID, fill=MUTED)
                y += 58
        d.text((140, 960), foot, font=SMALL, fill=YEL)
        self.frame = im.tobytes()
        for _ in range(round(sec * FPS)):
            self.ff.stdin.write(self.frame)
        self.seconds += sec

    def close(self) -> float:
        self.ff.stdin.close()
        self.ff.wait()
        return self.seconds


def rel(path: str, stage: str) -> str:
    return path.split(stage + "/", 1)[-1] if stage and stage in path else Path(path).name


def tool_label(name: str, inp: dict, stage: str) -> str:
    if name in ("Read", "Write", "Edit", "NotebookEdit"):
        return f"{'Update' if name == 'Edit' else name}({rel(inp.get('file_path', ''), stage)})"
    if name == "Bash":
        cmd = " ".join(inp.get("command", "").split())
        return f"Bash({cmd[:64] + '…' if len(cmd) > 65 else cmd})"
    if name in ("Glob", "Grep"):
        return f"{name}({inp.get('pattern', '')[:50]})"
    if name in ("Agent", "Task"):
        return f"{inp.get('subagent_type') or 'agent'}({inp.get('description', '')[:50]})"
    if name == "Skill":
        return f"Skill({inp.get('skill', inp.get('command', ''))})"
    if name == "TodoWrite":
        return "Update todos"
    if name == "SendMessage":
        return f"SendMessage({inp.get('summary', '')[:60]})"
    return f"{name}"


def result_text(block: dict) -> str:
    content = block.get("content")
    if isinstance(content, list):
        content = "\n".join(c.get("text", "") for c in content if isinstance(c, dict))
    return ANSI.sub("", str(content or ""))


def load_turn(path: Path) -> tuple[list[dict], str]:
    events, stage = [], ""
    for line in path.read_text().splitlines():
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            continue
        if e.get("type") == "system" and e.get("subtype") == "init":
            stage = e.get("cwd", "")
        events.append(e)
    return events, stage


def steps(events: list[dict]) -> tuple[list[tuple[str, dict]], str]:
    """Flatten to tool / text / hook steps in transcript order and return the final assistant text."""
    out, results, final = [], {}, ""
    for e in events:
        msg = e.get("message")
        if e.get("type") == "user" and isinstance(msg, dict) and isinstance(msg.get("content"), list):
            for b in msg["content"]:
                if b.get("type") == "tool_result":
                    results[b.get("tool_use_id")] = (result_text(b), bool(b.get("is_error")))
    for e in events:
        msg = e.get("message")
        if e.get("type") == "system" and e.get("subtype") == "hook_response":
            name, code = e.get("hook_name", ""), e.get("exit_code")
            if name.startswith("PostToolUse") or code == 2:
                out.append(("hook", {"name": name, "code": code, "stderr": e.get("stderr", "")}))
        if e.get("type") != "assistant" or not isinstance(msg, dict):
            continue
        for b in msg.get("content", []):
            if b.get("type") == "tool_use":
                out.append(("tool", {"name": b["name"], "input": b.get("input", {}), "result": results.get(b.get("id"), ("", False))}))
            elif b.get("type") == "text" and b.get("text", "").strip():
                out.append(("text", {"text": b["text"].strip()}))
                final = b["text"].strip()
    while out and out[-1][0] in ("text", "hook"):
        if out[-1][0] == "text":
            out.pop()
            break
        out.pop()
    return out, final


def show_hook(m: Movie, step: dict) -> None:
    if step["code"] == 2:
        reason = next((l for l in step["stderr"].splitlines() if l.strip()), "blocked")
        m.add(f"  ✗ {step['name']} hook blocked (exit 2): {reason}"[:COLS], RED, True)
        m.hold(2.5)
    elif step["code"] == 0:
        m.add(f"  ✓ {step['name']} hook: post-edit validation passed (exit 0)"[:COLS], GREEN)
        m.hold(0.4)
    else:
        m.add(f"  ! {step['name']} hook exit {step['code']}"[:COLS], YEL)
        m.hold(0.6)


def clean_md(text: str) -> str:
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    return re.sub(r"^#+\s*", "", text, flags=re.M)


def show_tool(m: Movie, step: dict, stage: str) -> None:
    name, inp = step["name"], step["input"]
    m.add("● " + tool_label(name, inp, stage), "white", True)
    text, is_error = step["result"]
    if name == "Edit":
        old = inp.get("old_string", "").splitlines()[:4]
        new = inp.get("new_string", "").splitlines()[:6]
        for line in old:
            m.add("- " + line, RED, indent=2)
        for line in new:
            m.add("+ " + line, GREEN, indent=2)
        m.hold(1.4)
        return
    if name == "Write":
        m.add(f"└ Wrote {len(inp.get('content', '').splitlines())} lines", MUTED, indent=2)
    elif name == "Bash":
        tail = [l for l in text.splitlines() if l.strip()][-4:]
        color = RED if is_error else MUTED
        for line in tail:
            m.add("└ " + line[:COLS - 4], GREEN if re.search(r"\bOK\b|Ran \d+ tests|# pass|passed", line) else color, indent=2)
    elif name in ("Agent", "Task"):
        first = next((l for l in text.splitlines() if l.strip()), "")
        if first:
            m.add("└ " + first[:COLS - 4], MUTED, indent=2)
    elif is_error:
        m.add("└ " + text.splitlines()[0][:COLS - 4] if text else "└ error", RED, indent=2)
    m.hold(0.9 if name in ("Bash", "Agent", "Task") else 0.5)


def render(n: int) -> Path:
    part = next(p for p in PARTS if p["n"] == n)
    evidence = ROOT / "parts" / part["slug"] / "evidence" / "recorded-run"
    summary = json.loads((evidence / "summary.json").read_text())
    out = ROOT / "videos" / f"{part['slug']}.mp4"
    out.parent.mkdir(exist_ok=True)
    m = Movie(out, f"PART {n:02d} · {part['title'].upper()}", "RECORDED REAL RUN · CLAUDE CODE 2.1.296")
    turns = [t for t in summary["turns"]]
    sub = part["project"] + (f"\n{CARD_NOTES[n]}" if n in CARD_NOTES else "")
    m.card(f"Part {n:02d} · {part['title']}", sub,
           "Recorded headless run of the exact prompts · real tool calls, real output · condensed for time", 5)
    for i, turn in enumerate(turns, start=1):
        for step in turn.get("human_steps", []):
            m.term, m.lines = "Terminal B · human step (engineer of record)", []
            m.caption = step["description"]
            m.typed("$ ", step["command"], LIME)
            for line in step["output"].strip().splitlines()[:12]:
                m.add(line, TXT)
                m.hold(0.25)
            m.hold(4)
        events, stage = load_turn(evidence / f"turn{i}.jsonl")
        flow, final = steps(events)
        m.term, m.lines = f"Terminal A · claude {'--permission-mode plan' if turn['options'].get('mode') == 'plan' else ''}".strip() + " · shipyard", []
        flags = " ".join(turn["options"].get("flags", []))
        envs = " ".join(f"{k}={v}" for k, v in turn["options"].get("env", {}).items())
        m.add(" Claude Code · Sonnet · ~/shipyard-stage" + (f" · {flags}" if flags else ""), LIME, True)
        if envs:
            m.add(" " + envs, YEL)
        if turn["options"].get("mode") == "plan":
            m.add(" ▸ plan mode on: read-only until the plan is approved", CYAN)
        m.add("─" * COLS, "#334155")
        m.caption = f"Prompt {i}: {turn['label']}"
        m.hold(0.6)
        m.typed("❯ ", turn["prompt"], "white")
        tools = [s for s in flow if s[0] == "tool"]
        keep = set(range(len(tools))) if len(tools) <= 12 else set(range(6)) | set(range(len(tools) - 6, len(tools)))
        m.caption = "Claude works: every line below is a real tool call from the transcript"
        ti, skipped = 0, 0
        for kind, step in flow:
            if kind == "hook":
                if ti - 1 in keep or step["code"] == 2:
                    show_hook(m, step)
                continue
            if kind == "tool":
                if ti in keep:
                    if skipped:
                        m.add(f"  … {skipped} more tool calls (condensed) …", MUTED)
                        m.hold(0.6)
                        skipped = 0
                    show_tool(m, step, stage)
                else:
                    skipped += 1
                ti += 1
        m.lines.append(("", TXT, False))
        m.caption = "Claude's own summary. Compare every claim with the evidence above."
        m.add("● " + clean_md(final.splitlines()[0])[:COLS - 2] if final else "●", LIME, True)
        m.hold(0.8)
        m.para(clean_md("\n".join(final.splitlines()[1:])), limit=13)
        cost = turn.get("cost_usd")
        m.add(f"✻ Turn finished in {turn.get('seconds', '?')} s" + (f" · ${cost:.2f}" if cost else ""), MUTED)
        m.hold(4.5)
    m.term, m.lines = "Terminal B · verification (bin/bootcamp verify)", []
    m.caption = "Independent check after the run: the part's acceptance checks"
    verify = ANSI.sub("", (evidence / "verify.txt").read_text()).strip().splitlines()
    m.typed("$ ", "bin/bootcamp verify", LIME)
    for line in verify:
        color = GREEN if "PASS" in line else RED if "FAIL" in line else TXT
        m.add(line, color, "PASS" in line or "FAIL" in line)
        m.hold(0.4)
    status = (evidence / "git-status.txt").read_text().strip().splitlines()
    m.typed("$ ", "git status --short", LIME)
    for line in status[:10] or ["(clean)"]:
        m.add(line, YEL)
        m.hold(0.25)
    m.add("")
    m.add("Nothing committed. The engineer of record reviews and decides.", LIME, True)
    m.hold(5)
    seconds = m.close()
    print(f"{out.name}: {seconds:.0f} s")
    return out


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        render(int(arg))
