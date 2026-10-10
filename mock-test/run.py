#!/usr/bin/env python3
"""Packt independent mock test for Claude Certified Associate - Foundations.

Claude Code Bootcamp: Cohort 2 (Packt, instructor Luca Berton).

Usage examples:
    python3 mock-test/run.py                         # full 60-question timed attempt
    python3 mock-test/run.py --shuffle               # shuffle answer options
    python3 mock-test/run.py --domain "Troubleshooting and Optimization"
    python3 mock-test/run.py --review                # print every question with answers
    python3 mock-test/run.py --time 90               # change the recommended time limit
    python3 mock-test/run.py --answers my.json       # grade a submission non-interactively

Python 3.9+ standard library only. Works on macOS, Linux and WSL.
"""

import argparse
import json
import os
import random
import sys
import textwrap
import time
from collections import Counter, OrderedDict
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_BANK = os.path.join(HERE, "questions.json")
DEFAULT_RESULTS_DIR = os.path.join(HERE, "results")
LETTERS = ["A", "B", "C", "D", "E"]

# Official domain weights from the workshop brief (percent of the mock test).
DOMAIN_WEIGHTS = OrderedDict([
    ("Prompting and Task Execution", 14),
    ("Output Evaluation and Validation", 21),
    ("Product and Model Selection", 12),
    ("Workflow Integration and Solution Design", 16),
    ("Configuration and Knowledge Management", 12),
    ("Governance, Risk, and Responsible Use", 15),
    ("Troubleshooting and Optimization", 10),
])

# Workshop alignment per domain (from the brief's Certification Alignment table).
DOMAIN_ALIGNMENT = {
    "Prompting and Task Execution":
        "Structured briefs, constraints, acceptance criteria, Best-of-N, and iterative prompting (workshop Parts 2 and 4)",
    "Output Evaluation and Validation":
        "Tests, browser verification, evidence review, security findings, and the Review Before Merge checklist (Parts 5, 7 and 12)",
    "Product and Model Selection":
        "Claude product surfaces, model selection, Claude Code, Cowork, Chrome, web, mobile, and Remote Control (Parts 1, 13 and 14)",
    "Workflow Integration and Solution Design":
        "Skills, hooks, subagents, plugins, Agent Teams, Git workflows, and stakeholder handoffs (Parts 6, 9, 10, 11 and 13)",
    "Configuration and Knowledge Management":
        "CLAUDE.md, scoped rules, auto memory, Skills, supporting files, and reusable project context (Parts 3 and 9)",
    "Governance, Risk, and Responsible Use":
        "Permissions, sandboxing, secrets, privacy, safe delegation, security review, and human approval (Parts 1, 6 and 12)",
    "Troubleshooting and Optimization":
        "Testing, debugging, checkpoints, rewind, /goal, context management, and workflow improvement (Parts 5 and 14)",
}

# Starting points when a domain has no missed questions to draw links from.
DOMAIN_CORE_DOCS = {
    "Prompting and Task Execution": [
        "https://code.claude.com/docs/en/best-practices",
        "https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices",
    ],
    "Output Evaluation and Validation": [
        "https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations",
        "https://platform.claude.com/docs/en/test-and-evaluate/develop-tests",
    ],
    "Product and Model Selection": [
        "https://platform.claude.com/docs/en/about-claude/models/choosing-a-model",
        "https://claude.com/docs/cowork/overview",
    ],
    "Workflow Integration and Solution Design": [
        "https://code.claude.com/docs/en/hooks-guide",
        "https://code.claude.com/docs/en/plugins",
    ],
    "Configuration and Knowledge Management": [
        "https://code.claude.com/docs/en/memory",
        "https://code.claude.com/docs/en/skills",
    ],
    "Governance, Risk, and Responsible Use": [
        "https://code.claude.com/docs/en/permissions",
        "https://code.claude.com/docs/en/security",
    ],
    "Troubleshooting and Optimization": [
        "https://code.claude.com/docs/en/checkpointing",
        "https://code.claude.com/docs/en/costs",
    ],
}

DISCLAIMER = (
    "IMPORTANT DISCLAIMER: This workshop and mock test are independently created by Packt. "
    "They are not official Anthropic training, are not endorsed by Anthropic, and do not contain "
    "official examination questions. Claude and Anthropic certification names are used only to "
    "identify the certification for which the materials provide independent preparation. "
    "Completion of the workshop or mock test does not guarantee success in the official "
    "certification examination."
)

SCALED_NOTE = (
    "The official examination uses scaled scoring, which cannot be reproduced precisely by an "
    "independent mock test. The mock test score does not guarantee success in the official examination."
)

READINESS_LEVELS = [
    (80.0, "Strong exam readiness"),
    (70.0, "Nearly ready, with focused revision recommended"),
    (60.0, "Additional study required"),
    (0.0, "Revisit the learning path before scheduling the official exam"),
]


# --------------------------------------------------------------------------- data

def load_bank(path=DEFAULT_BANK):
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    if isinstance(data, list):
        data = {"questions": data}
    return data


def resolve_domain(name, questions):
    """Return the exact domain name for NAME (exact, then case-insensitive unique match)."""
    domains = list(OrderedDict.fromkeys(q["domain"] for q in questions))
    if name in domains:
        return name
    low = name.strip().lower()
    exact_ci = [d for d in domains if d.lower() == low]
    if exact_ci:
        return exact_ci[0]
    partial = [d for d in domains if low in d.lower()]
    if len(partial) == 1:
        return partial[0]
    raise ValueError(
        "Unknown or ambiguous domain %r. Choose one of:\n  - %s" % (name, "\n  - ".join(domains))
    )


def filter_questions(questions, domain=None):
    if not domain:
        return list(questions)
    return [q for q in questions if q["domain"] == domain]


def parse_letters(raw):
    """Turn 'b', 'A,C', 'a c' or ['A','C'] into a sorted list of unique letters."""
    if raw is None:
        return []
    if isinstance(raw, (list, tuple)):
        raw = ",".join(str(x) for x in raw)
    out = []
    for ch in str(raw).upper():
        if ch in LETTERS and ch not in out:
            out.append(ch)
    return sorted(out)


def load_answers_file(path):
    """Load {"Q01": ["B"], ...}. Optional key "marked": ["Q05", ...]."""
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, dict):
        raise ValueError("Answers file must be a JSON object such as {\"Q01\": [\"B\"]}")
    marked = data.get("marked", data.get("_marked", [])) or []
    responses = {}
    for key, value in data.items():
        if key in ("marked", "_marked"):
            continue
        responses[key.strip().upper()] = parse_letters(value)
    return responses, [m.strip().upper() for m in marked]


# --------------------------------------------------------------------------- grading

def is_correct(question, letters):
    """Multiple-response questions score only when the selection is exactly right."""
    return sorted(letters) == sorted(question["answer"])


def readiness_level(percent):
    for threshold, label in READINESS_LEVELS:
        if percent >= threshold:
            return label
    return READINESS_LEVELS[-1][1]


def grade(questions, responses, marked=None, display_orders=None):
    """Grade RESPONSES ({id: [letters]}) against QUESTIONS. Letters are canonical."""
    marked = set(marked or [])
    display_orders = display_orders or {}
    items = []
    by_domain = OrderedDict()
    present = {q["domain"] for q in questions}
    for name in list(DOMAIN_WEIGHTS) + sorted(present - set(DOMAIN_WEIGHTS)):
        if name in present:
            by_domain[name] = {"correct": 0, "total": 0}
    for q in questions:
        given = parse_letters(responses.get(q["id"]))
        ok = is_correct(q, given)
        items.append({
            "question": q,
            "given": given,
            "correct": ok,
            "answered": bool(given),
            "marked": q["id"] in marked,
            "display_order": display_orders.get(q["id"], LETTERS[:]),
        })
        d = by_domain.setdefault(q["domain"], {"correct": 0, "total": 0})
        d["total"] += 1
        d["correct"] += int(ok)
    for d in by_domain.values():
        d["percent"] = round(100.0 * d["correct"] / d["total"], 1) if d["total"] else 0.0
    total = len(items)
    correct = sum(1 for i in items if i["correct"])
    percent = round(100.0 * correct / total, 1) if total else 0.0
    return {
        "items": items,
        "total": total,
        "correct": correct,
        "percent": percent,
        "level": readiness_level(percent),
        "by_domain": by_domain,
    }


def strongest_weakest(by_domain):
    if not by_domain:
        return [], []
    best = max(d["percent"] for d in by_domain.values())
    worst = min(d["percent"] for d in by_domain.values())
    strongest = [n for n, d in by_domain.items() if d["percent"] == best]
    weakest = [n for n, d in by_domain.items() if d["percent"] == worst]
    return strongest, weakest


def domain_priority(by_domain):
    """Domains ordered by weighted deficit: (1 - score) * exam weight, largest first."""
    scored = []
    for name, d in by_domain.items():
        weight = DOMAIN_WEIGHTS.get(name, 10)
        deficit = (100.0 - d["percent"]) / 100.0 * weight
        scored.append((deficit, -d["percent"], name))
    scored.sort(key=lambda t: (-t[0], t[1], t[2]))
    return [(name, deficit) for deficit, _, name in scored]


def allocate_days(by_domain, days=5):
    """Spread DAYS focus slots across domains, weighted toward the weakest.

    Every weakest domain (lowest score, below 100%) gets at least one day. The remaining days
    are shared in proportion to the weighted deficit, and the schedule runs weakest first.
    """
    prio = domain_priority(by_domain)
    deficits = dict(prio)
    total = sum(deficits.values())
    if total <= 0:
        # Perfect score: rotate through the most heavily weighted domains.
        names = sorted(by_domain, key=lambda n: -DOMAIN_WEIGHTS.get(n, 10))
        return [names[i % len(names)] for i in range(days)] if names else []
    _, weakest = strongest_weakest(by_domain)
    alloc = {name: 0 for name in by_domain}
    for name in weakest[:days]:
        if by_domain[name]["percent"] < 100:
            alloc[name] = 1
    remaining = days - sum(alloc.values())
    if remaining > 0:
        quotas = [(name, remaining * d / total) for name, d in prio]
        for name, q in quotas:
            alloc[name] += int(q)
        left = days - sum(alloc.values())
        for name, q in sorted(quotas, key=lambda t: (-(t[1] - int(t[1])), -deficits[t[0]])):
            if left <= 0:
                break
            alloc[name] += 1
            left -= 1
    order = sorted((n for n in alloc if alloc[n] > 0),
                   key=lambda n: (by_domain[n]["percent"], -deficits[n], n))
    schedule = []
    for name in order:
        schedule.extend([name] * alloc[name])
    return schedule[:days]


# --------------------------------------------------------------------------- report

def _display_letter(item, canonical):
    order = item["display_order"]
    return LETTERS[order.index(canonical)] if canonical in order else canonical


def _fmt_choice(item, letters):
    if not letters:
        return "(no answer)"
    q = item["question"]
    parts = []
    for l in sorted(letters, key=lambda c: _display_letter(item, c)):
        parts.append("%s. %s" % (_display_letter(item, l), q["options"][l]))
    return "; ".join(parts)


def recommended_docs(result):
    counts = Counter()
    first_seen = {}
    for item in result["items"]:
        if item["correct"]:
            continue
        for link in item["question"].get("doc_links", []):
            counts[link] += 1
            first_seen.setdefault(link, len(first_seen))
    return sorted(counts.items(), key=lambda kv: (-kv[1], first_seen[kv[0]]))


def seven_day_plan(result):
    by_domain = result["by_domain"]
    missed = {}
    for item in result["items"]:
        if not item["correct"]:
            missed.setdefault(item["question"]["domain"], []).append(item["question"]["id"])
    marked = [i["question"]["id"] for i in result["items"] if i["marked"]]
    schedule = allocate_days(by_domain, days=5)
    lines = []
    seen_count = Counter()
    for day, name in enumerate(schedule, start=1):
        seen_count[name] += 1
        d = by_domain[name]
        ids = missed.get(name, [])
        docs = []
        for item in result["items"]:
            if item["question"]["domain"] == name and not item["correct"]:
                for link in item["question"].get("doc_links", []):
                    if link not in docs:
                        docs.append(link)
        if not docs:
            docs = DOMAIN_CORE_DOCS.get(name, [])
        part = " (session %d)" % seen_count[name] if schedule.count(name) > 1 else ""
        lines.append("**Day %d: %s%s** (your score %d/%d, %.0f%%; exam weight %d%%)" % (
            day, name, part, d["correct"], d["total"], d["percent"], DOMAIN_WEIGHTS.get(name, 0)))
        lines.append("- Workshop material: %s." % DOMAIN_ALIGNMENT.get(name, "review the related workshop part"))
        if ids:
            if seen_count[name] == 1:
                lines.append("- Re-read the explanations for every option in: %s. Write down, in your own words, why each distractor is wrong." % ", ".join(ids))
            else:
                lines.append("- Without looking at the answers, re-attempt %s, then check your reasoning against the explanations." % ", ".join(ids))
        else:
            lines.append("- No missed questions here: skim the explanations for this domain to consolidate, then focus on edge cases.")
        lines.append("- Read: %s" % ", ".join(docs[:3]))
        lines.append("- Practise: `python3 mock-test/run.py --domain \"%s\" --shuffle`" % name)
        lines.append("")
    lines.append("**Day 6: Mixed review**")
    if marked:
        lines.append("- Revisit the questions you marked for review: %s." % ", ".join(marked))
    lines.append("- Run `python3 mock-test/run.py --review` and scan every explanation for topics you could not explain to a colleague.")
    lines.append("- Redo one hands-on workshop lab that maps to your weakest domain, and capture real evidence (test output, diff, screenshot).")
    lines.append("")
    lines.append("**Day 7: Timed retake**")
    lines.append("- Take the full test again under the 120-minute recommended limit: `python3 mock-test/run.py --shuffle`.")
    lines.append("- Compare the new report with this one: domain scores should rise in the areas you studied.")
    return "\n".join(lines)


def retake_recommendation(result):
    pct = result["percent"]
    low = [n for n, d in result["by_domain"].items() if d["percent"] < 60]
    if pct >= 80:
        rec = ("Optional. You are showing strong readiness. Retake once with --shuffle after a few days to "
               "confirm the result is stable, then consider scheduling the official exam.")
    elif pct >= 70:
        rec = ("Yes, after 3 to 5 days of focused revision on your weakest domains. Aim for 80% or higher "
               "on the retake before scheduling the official exam.")
    elif pct >= 60:
        rec = ("Yes, after completing the full seven-day revision plan. Use --domain practice on weak "
               "domains first, then take a full timed retake.")
    else:
        rec = ("Yes, but only after revisiting the learning path (workshop recordings, labs and the official "
               "documentation listed above) and completing the seven-day plan. Do not schedule the official "
               "exam yet.")
    if low:
        rec += " Domains below 60%% need targeted practice first: %s." % ", ".join(low)
    return rec


def build_report(result, meta=None):
    meta = meta or {}
    strongest, weakest = strongest_weakest(result["by_domain"])
    out = []
    out.append("# Certification Readiness Report")
    out.append("")
    out.append("Claude Certified Associate - Foundations: Packt independent mock test "
               "(Claude Code Bootcamp: Cohort 2)")
    out.append("")
    out.append("- Date: %s" % meta.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    out.append("- Mode: %s" % meta.get("mode", "interactive"))
    if meta.get("domain"):
        out.append("- Domain practice: %s" % meta["domain"])
    if meta.get("elapsed_seconds") is not None:
        out.append("- Time taken: %s (recommended limit %d minutes)" % (
            _fmt_duration(meta["elapsed_seconds"]), meta.get("time_limit", 120)))
    if meta.get("shuffle"):
        out.append("- Options were shuffled: letters below are the ones shown to you during the attempt.")
    out.append("")
    out.append("> %s" % DISCLAIMER)
    out.append("")

    out.append("## Overall score")
    out.append("")
    out.append("**%d / %d correct (%.1f%%)**" % (result["correct"], result["total"], result["percent"]))
    out.append("")
    out.append("Readiness level: **%s**" % result["level"])
    out.append("")
    out.append("| Score band | Readiness level |")
    out.append("|---|---|")
    out.append("| 80% or higher | Strong exam readiness |")
    out.append("| 70% to 79% | Nearly ready, with focused revision recommended |")
    out.append("| 60% to 69% | Additional study required |")
    out.append("| Below 60% | Revisit the learning path before scheduling the official exam |")
    out.append("")
    out.append("_%s_" % SCALED_NOTE)
    out.append("")

    out.append("## Score by certification domain")
    out.append("")
    out.append("| Domain | Correct | Questions | Score | Exam weight |")
    out.append("|---|---|---|---|---|")
    for name, d in result["by_domain"].items():
        out.append("| %s | %d | %d | %.0f%% | %d%% |" % (
            name, d["correct"], d["total"], d["percent"], DOMAIN_WEIGHTS.get(name, 0)))
    out.append("")
    if len(result["by_domain"]) > 1:
        out.append("- **Strongest domain:** %s" % ", ".join(strongest))
        out.append("- **Weakest domain:** %s" % ", ".join(weakest))
    else:
        out.append("- Single-domain practice: take the full test to see strongest and weakest domains.")
    out.append("")

    out.append("## Questions marked for review")
    out.append("")
    marked = [i for i in result["items"] if i["marked"]]
    if marked:
        for item in marked:
            q = item["question"]
            out.append("- %s (%s): %s" % (q["id"], q["domain"], "correct" if item["correct"] else "incorrect"))
    else:
        out.append("- None. (Type `m` during an interactive attempt to mark a question.)")
    out.append("")

    out.append("## Explanation of incorrect answers")
    out.append("")
    wrong = [i for i in result["items"] if not i["correct"]]
    if not wrong:
        out.append("No incorrect answers. Well done.")
        out.append("")
    for item in wrong:
        q = item["question"]
        out.append("### %s: %s%s" % (q["id"], q["domain"], " (marked)" if item["marked"] else ""))
        out.append("")
        out.append("_Scenario:_ %s" % q["scenario"])
        out.append("")
        out.append("_Question:_ %s" % q["question"])
        out.append("")
        out.append("- Your answer: %s" % _fmt_choice(item, item["given"]))
        out.append("- Correct answer: %s" % _fmt_choice(item, q["answer"]))
        out.append("")
        for l in sorted(q["answer"], key=lambda c: _display_letter(item, c)):
            out.append("  - Why %s is right: %s" % (_display_letter(item, l), q["explanations"][l]))
        for l in sorted(item["given"], key=lambda c: _display_letter(item, c)):
            if l not in q["answer"]:
                out.append("  - Why %s is wrong: %s" % (_display_letter(item, l), q["explanations"][l]))
        if q.get("doc_links"):
            out.append("  - Documentation: %s" % ", ".join(q["doc_links"]))
        out.append("")

    out.append("## Recommended official documentation")
    out.append("")
    docs = recommended_docs(result)
    if docs:
        for link, n in docs:
            out.append("- %s (linked to %d missed question%s)" % (link, n, "" if n == 1 else "s"))
    else:
        out.append("No missed questions. Keep these core references fresh:")
        for name in result["by_domain"]:
            for link in DOMAIN_CORE_DOCS.get(name, []):
                out.append("- %s (%s)" % (link, name))
    out.append("")

    out.append("## Suggested seven-day revision plan")
    out.append("")
    out.append("Days 1 to 5 are weighted toward the domains where your score gap, multiplied by the domain's "
               "exam weight, is largest.")
    out.append("")
    out.append(seven_day_plan(result))
    out.append("")

    out.append("## Should you attempt the mock test again?")
    out.append("")
    out.append(retake_recommendation(result))
    out.append("")
    out.append("---")
    out.append("")
    out.append(DISCLAIMER)
    out.append("")
    return "\n".join(out)


def write_report(text, results_dir=DEFAULT_RESULTS_DIR, timestamp=None):
    os.makedirs(results_dir, exist_ok=True)
    stamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    path = os.path.join(results_dir, "%s.md" % stamp)
    n = 1
    while os.path.exists(path):
        n += 1
        path = os.path.join(results_dir, "%s-%d.md" % (stamp, n))
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return path


# --------------------------------------------------------------------------- terminal UI

def _fmt_duration(seconds):
    seconds = int(max(0, seconds))
    return "%d:%02d:%02d" % (seconds // 3600, (seconds % 3600) // 60, seconds % 60)


def _wrap(text, indent="", hang=""):
    width = 100
    try:
        width = min(100, os.get_terminal_size().columns - 2)
    except OSError:
        pass
    return textwrap.fill(text, width=max(40, width), initial_indent=indent, subsequent_indent=indent + hang)


def print_question(q, position, total, order=None, show_answer=False):
    order = order or LETTERS
    kind = "Single answer" if q["type"] == "single" else "Select %d" % len(q["answer"])
    print("")
    print("=" * 72)
    print("%s  [%d/%d]  %s  |  %s  |  %s" % (q["id"], position, total, q["domain"], kind, q["difficulty"]))
    print("-" * 72)
    print(_wrap(q["scenario"]))
    print("")
    print(_wrap(q["question"]))
    print("")
    for shown, canonical in zip(LETTERS, order):
        print(_wrap("%s. %s" % (shown, q["options"][canonical]), indent="  ", hang="   "))
    if show_answer:
        correct = [LETTERS[order.index(c)] for c in q["answer"]]
        print("")
        print("Answer: %s" % ", ".join(sorted(correct)))
        for shown, canonical in zip(LETTERS, order):
            print(_wrap("%s: %s" % (shown, q["explanations"][canonical]), indent="    ", hang="   "))
        if q.get("doc_links"):
            print("    Docs: %s" % ", ".join(q["doc_links"]))


def run_review(questions):
    print(DISCLAIMER)
    for pos, q in enumerate(questions, start=1):
        print_question(q, pos, len(questions), show_answer=True)
    print("")
    print(DISCLAIMER)


def run_interactive(questions, time_limit_min, shuffle, seed=None, input_fn=input):
    rng = random.Random(seed)
    orders = {}
    for q in questions:
        order = LETTERS[:]
        if shuffle:
            rng.shuffle(order)
        orders[q["id"]] = order
    responses, marked = {}, set()
    start = time.time()
    deadline = start + time_limit_min * 60
    warned = False
    print("")
    print("Answer with letters (e.g. B, or A C for 'Select 2'). Add or type 'm' to mark for review,")
    print("'s' to skip, 'q' to finish early. The time limit is a recommendation; nothing is cut off.")
    for pos, q in enumerate(questions, start=1):
        order = orders[q["id"]]
        print_question(q, pos, len(questions), order=order)
        need = len(q["answer"])
        while True:
            remaining = deadline - time.time()
            if remaining <= 0 and not warned:
                print("\n*** Recommended %d-minute limit reached. You may continue. ***" % time_limit_min)
                warned = True
            clock = "Time left %s" % _fmt_duration(remaining) if remaining > 0 else "Over time +%s" % _fmt_duration(-remaining)
            flag = " [marked]" if q["id"] in marked else ""
            try:
                raw = input_fn("[%s]%s Your answer: " % (clock, flag))
            except (EOFError, KeyboardInterrupt):
                print("\nFinishing early.")
                return responses, marked, orders, time.time() - start
            text = raw.strip().lower()
            if text == "q":
                return responses, marked, orders, time.time() - start
            if text == "s":
                break
            tokens = text.replace(",", " ").split()
            if "m" in tokens or text == "m":
                if q["id"] in marked and tokens == ["m"]:
                    marked.discard(q["id"])
                    print("Unmarked.")
                else:
                    marked.add(q["id"])
                    print("Marked for review.")
                tokens = [t for t in tokens if t != "m"]
                if not tokens:
                    continue
            shown = parse_letters("".join(tokens))
            if not shown or any(ch not in "abcde" for ch in "".join(tokens)):
                print("Please enter option letters A-E (or m / s / q).")
                continue
            if len(shown) != need:
                print("This question needs exactly %d letter%s." % (need, "" if need == 1 else "s"))
                continue
            responses[q["id"]] = sorted(order[LETTERS.index(l)] for l in shown)
            break
    return responses, marked, orders, time.time() - start


# --------------------------------------------------------------------------- main

def build_parser():
    p = argparse.ArgumentParser(
        description="Packt independent mock test for Claude Certified Associate - Foundations.")
    p.add_argument("--domain", help="practise one domain (exact name, or a unique part of it)")
    p.add_argument("--shuffle", action="store_true", help="shuffle answer options for each question")
    p.add_argument("--seed", type=int, help="random seed for --shuffle (reproducible order)")
    p.add_argument("--review", action="store_true", help="print all questions with answers and explanations")
    p.add_argument("--time", type=int, default=120, metavar="MINUTES",
                   help="recommended time limit shown as a countdown (default 120; no hard stop)")
    p.add_argument("--answers", metavar="FILE", help="grade a JSON submission non-interactively")
    p.add_argument("--bank", default=DEFAULT_BANK, help=argparse.SUPPRESS)
    p.add_argument("--results-dir", default=DEFAULT_RESULTS_DIR, help="where to write the report")
    p.add_argument("--no-save", action="store_true", help="print the report without writing a file")
    p.add_argument("--list-domains", action="store_true", help="list domains and question counts")
    return p


def main(argv=None, input_fn=input):
    args = build_parser().parse_args(argv)
    bank = load_bank(args.bank)
    questions = bank["questions"]

    if args.list_domains:
        counts = Counter(q["domain"] for q in questions)
        for name, weight in DOMAIN_WEIGHTS.items():
            print("%-45s %2d questions  (%d%%)" % (name, counts.get(name, 0), weight))
        return 0

    domain = None
    if args.domain:
        try:
            domain = resolve_domain(args.domain, questions)
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            return 2
    selected = filter_questions(questions, domain)
    if args.time <= 0:
        print("--time must be a positive number of minutes", file=sys.stderr)
        return 2

    if args.review:
        run_review(selected)
        return 0

    print(DISCLAIMER)
    print("")
    meta = {"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "domain": domain,
            "time_limit": args.time, "shuffle": False}

    if args.answers:
        try:
            responses, marked = load_answers_file(args.answers)
        except (OSError, ValueError) as exc:
            print("Could not read answers file: %s" % exc, file=sys.stderr)
            return 2
        known = {q["id"] for q in questions}
        unknown = sorted(k for k in responses if k not in known)
        if unknown:
            print("Warning: ignoring unknown question ids: %s" % ", ".join(unknown), file=sys.stderr)
        meta["mode"] = "non-interactive grading of %s" % os.path.basename(args.answers)
        result = grade(selected, responses, marked)
    else:
        print("%d questions | recommended time %d minutes | %s" % (
            len(selected), args.time, domain or "all seven domains"))
        responses, marked, orders, elapsed = run_interactive(
            selected, args.time, args.shuffle, seed=args.seed, input_fn=input_fn)
        meta.update({"mode": "interactive", "elapsed_seconds": elapsed, "shuffle": args.shuffle})
        result = grade(selected, responses, marked, display_orders=orders)

    report = build_report(result, meta)
    print("")
    print(report)
    if not args.no_save:
        path = write_report(report, args.results_dir)
        print("Report saved to %s" % path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
