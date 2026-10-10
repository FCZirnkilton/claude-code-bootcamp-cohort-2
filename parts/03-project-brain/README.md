# Part 03 · CLAUDE.md, scoped rules and auto memory

**Project 3: Project Brain** · 25 minutes · 09:45–10:10 (brief schedule)

## Learning goals
- Decide what belongs in CLAUDE.md, and what does not
- Record build/test commands, conventions, security rules and do-not-touch areas concisely
- Use .claude/rules with `paths:` for directory- or language-specific instructions
- Move occasional reference material into Skills
- Review, correct and remove stale auto memory

## Learners leave with
- Reusable CLAUDE.md (under 60 lines)
- Path-scoped rules (`tests/**`, `shipctl.py`)
- Documented conventions
- Reviewed auto-memory entry
- Evidence that Claude followed the context (`shipctl stats`)

## Run it
```sh
# terminal B (this bootcamp repo)
bin/bootcamp stage 03      # fresh Shipyard repo at ~/shipyard-stage + baseline commit
# terminal A
cd ~/shipyard-stage && claude --model sonnet
# ... paste the prompts from PROMPTS.md ...
# terminal B
bin/bootcamp verify           # acceptance checks on ~/shipyard-stage
```

## Timing inside the part
- 4 min: topic slides
- 5 min: live demo or recorded video (deck)
- 6 min: explain and discuss
- rest: hands-on lab

## Lab
Write CLAUDE.md and the rules (Claude Code asks you to approve edits under .claude/: read them, then approve), start a fresh session, request the `stats` change, and check the diff against the rules. Open `/memory` and remove one stale entry.

## Evidence to show (not claims)
- `/memory` shows CLAUDE.md, rules and auto memory
- `/context` shows what loaded
- Diff of `stats` follows `cmd_` naming, README table, test class conventions
- Reviewed memory entries in docs/memory-review.md

## Discussion
- What did you delete from your first CLAUDE.md draft, and why?
- When is a path-scoped rule better than a line in CLAUDE.md?
- Which auto-memory entries would you never keep?

## If it goes wrong
- Load the prepared reference: `bin/bootcamp fallback 03` (say clearly that it is prepared, not live).
- Or jump to the full reference state: `bin/bootcamp checkpoint 03 --force`.
- Play the recorded run in the deck (video `03`): Claude writes CLAUDE.md and two scoped rules, then implements `stats` and cites the rules it applied.

## Files
- `start/` — overlay that creates the starting state (briefs, inputs)
- `solution/` — overlay that creates the reference checkpoint
- `evidence/` — captured screenshots, outputs and the recorded Claude Code run (`recorded-run/`)
