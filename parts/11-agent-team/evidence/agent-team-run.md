# Recorded run: release notes sprint (Part 11)

**What this recording is.** A real headless run (`claude -p`, Sonnet, `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`) of the two prompts in `PROMPTS.md`. In print mode there is no interactive team UI, so the lead coordinated **parallel background agents**. That gives the same workflow as the brief (frozen contract → read-only plans → approval → parallel implementation → steering), but not the interactive Agent Team panes and shared task list. The interactive Agent Team is the instructor's live demo; this transcript, the task board and the diff are the fallback material the brief asks for.

## What happened (from `recorded-run/turn1.jsonl`, `turn2.jsonl`)
1. The lead read the brief, froze the API contract and wrote `docs/team-plan.md` (task board with owners and dependencies).
2. Three planning agents ran in parallel (`subagent_type: Plan`, read-only): backend, frontend, test and verification.
3. The lead checked each plan against the ownership table before approving. The backend plan added a `400` for an unknown `format` value, which the lead accepted explicitly.
4. Three implementers ran in parallel with their approved plans.
5. Turn 2: the lead steered the running frontend owner with `SendMessage` (empty state + 1.5 s "Copied").
6. The lead reported honestly that the browser check and `/engineering-quality:change-review` had **not** been run yet. Those remain human/lead steps before acceptance.

## Facts
| | |
|---|---|
| Wall time | 851 s over 2 prompts |
| Cost | $2.21 |
| Tool calls by the lead | 70 |
| Last test summary seen | # pass 21 |
| `bin/bootcamp verify` | 20 PASS, 0 FAIL |

## Files changed (owner files from the brief, plus the lead's docs/team-plan.md)
| File | Change |
|---|---|
| `dashboard/index.html` | modified |
| `dashboard/js/main.js` | modified |
| `dashboard/styles.css` | modified |
| `notes_api/server.py` | modified |
| `dashboard/js/release-notes.js` | new |
| `dashboard/tests/release-notes.test.mjs` | new |
| `docs/team-plan.md` | new |
| `notes_api/releases.py` | new |
| `tests/test_release_notes.py` | new |

## Retrospective prompts for learners
- Which plan would you have rejected, and why?
- The lead didn't run the browser check. What should the quality gate have required before "done"?
- Was a team worth $2.21 for this change? Estimate the single-session cost.
