# Claude Code Bootcamp: Cohort 2

**Build, orchestrate, review, and ship with 10 new advanced hands-on projects in one day.**
Packt live virtual workshop · Instructor: Luca Berton · 7.5 hours (6 h + 30 min Q&A + 30 min breaks) · Beginner to intermediate

> Build faster. Orchestrate smarter. Verify everything. Ship with confidence.

Learners build one product, **Shipyard** (a release-management toolkit), across 10 connected projects: a CLI, a Notes API, a release dashboard, a quality plugin, an Agent Team feature, a production review and a stakeholder handoff. Every step ends with evidence, not a claim.

## Quick start

```sh
bin/bootcamp preflight          # tools + every reference checkpoint builds and passes its tests
bin/bootcamp list               # the 14 parts
bin/bootcamp stage 01           # Shipyard at ~/shipyard-stage, with a baseline commit
cd ~/shipyard-stage && claude --model sonnet
```

Requirements: Python 3.10+, Git, Node.js 18+ (dashboard tests), Claude Code (logged in), Chrome for Part 7, a GitHub account for selected workflows. macOS, Linux or WSL2.

## What is in this repository

| Path | Contents |
|---|---|
| `deck/claude-code-bootcamp-cohort-2.pptx` | The presenter deck: per part → topic slides, exact prompt, **embedded recorded video**, evidence, discussion, lab, checkpoint |
| `videos/` | One recording per part: real headless Claude Code runs of the exact prompts, rendered in a large font |
| `parts/NN-*/` | Instructor runbook (`README.md`), copy-paste `PROMPTS.md`, `start/` and `solution/` overlays, `evidence/` (screenshots, outputs, raw transcripts) |
| `bin/bootcamp` | `stage`, `checkpoint`, `fallback`, `verify`, `preflight`, `diff` for every part |
| `skills-pack/` | The attendee Skills Pack: 8 skills, 2 subagents, 3 hooks, installer |
| `plugins/engineering-quality/` + `.claude-plugin/marketplace.json` | The Part 10 plugin, installable from this repo as a marketplace |
| `templates/` | Decision matrix, Rejected Options Log, Review Before Merge, readiness report, stakeholder update, routine brief and more |
| `assessment/` | Quiz (30%), capstone (50%), reflection (20%), rubric, grading sheet |
| `mock-test/` | 60-question certification mock test with readiness report (`python3 mock-test/run.py`) |
| `docs/` | `RUN-OF-SHOW.md`, `PRESENTER-CUE-CARD.md`, `FEATURE-REFERENCE.md` (verified Claude Code syntax), `BRIEF.md` (the original brief) |
| `tools/` | Course data (single source of truth), runbook generator, run recorder |

## The 14 parts

| # | Time | Part | Project |
|---|---|---|---|
| 01 | 09:00 | Welcome, setup, AI-first mindset and safe delegation | 1 · AI-Ready Engineering Workspace |
| 02 | 09:20 | Prompting Claude Code like a tech lead | 2 · CLI Release Task Manager |
| 03 | 09:45 | CLAUDE.md, scoped rules and auto memory | 3 · Project Brain |
| 04 | 10:20 | Best-of-N and better engineering decisions | 4 · Notes API Design Tournament |
| 05 | 10:50 | Testing, debugging, checkpoints and /goal | 5 · Resilient Notes API |
| 06 | 11:20 | Git workflows, worktrees, permissions and sandboxing | 6 · Isolated Search Feature |
| 07 | 11:55 | Multimodal building and Chrome verification | 7 · Dashboard from a Wireframe |
| 08 | 13:00 | Refactor, document and create a maintainer handoff | 8 · Maintainer-Ready Dashboard |
| 09 | 13:20 | Skills, hooks and specialist subagents | 9A · Engineering Quality Skills Pack |
| 10 | 13:55 | Plugins and marketplace distribution | 9B · Engineering Quality Plugin |
| 11 | 14:20 | Agent Teams: ship a feature in parallel | 9C · Parallel Feature Sprint |
| 12 | 15:00 | Production readiness, security and code review | 10A · Production Readiness Review |
| 13 | 15:25 | Claude Cowork: engineering output to stakeholder update | 10B · Stakeholder Handoff |
| 14 | 15:45 | Web, mobile, Remote Control and work that continues | 10C · Cross-Device Continuation |
| – | 16:05 | Final Q&A and exam briefing | – |

Times follow the brief's schedule table (450 minutes). If the cohort starts at 10:00 ET, shift every time by one hour (`START` in `tools/course_data.py`, then rebuild).

## How the checkpoints work

Each part has a `start/` overlay (briefs, inputs) and a `solution/` overlay (reference result). `bin/bootcamp` layers them, so every part starts exactly where the previous one ended, and anyone who falls behind catches up with one command:

```sh
bin/bootcamp stage 05            # start of part 05
bin/bootcamp fallback 05         # load the prepared reference into your stage (say so if used live)
bin/bootcamp checkpoint 05 --force   # jump straight to the end of part 05
bin/bootcamp verify              # acceptance checks on ~/shipyard-stage
```

## Rebuild the materials

```sh
python3 tools/gen_parts.py                       # part runbooks + prompts from tools/course_data.py
python3 tools/record_run.py 05                   # re-record a part with real headless Claude Code
python3 deck/video/render_run.py 05              # render its video (needs Pillow + ffmpeg)
python3 deck/build_deck.py                       # rebuild the deck (needs python-pptx + ffmpeg)
```

## Disclaimer

This workshop and its mock test are independently created by Packt. They are not official Anthropic training, are not endorsed by Anthropic, and do not contain official examination questions. Completion does not guarantee success in any official certification examination.
