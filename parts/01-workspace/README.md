# Part 01 · Welcome, setup, AI-first mindset and safe delegation

**Project 1: AI-Ready Engineering Workspace** · 20 minutes · 09:00–09:20 (brief schedule)

## Learning goals
- Map what Claude Code can do across CLI, IDE, desktop, web and mobile
- Run the lifecycle: plan → implement → verify → review → commit
- Choose model, context and effort for a task
- Pick a permission mode and accept workspace trust deliberately
- Separate reversible from irreversible actions; create a recovery point first

## Learners leave with
- Working Claude Code environment
- Trusted starter repository
- Written permission and safety boundary (SAFETY.md + .claude/settings.json)
- Baseline Git commit and recovery point

## Run it
```sh
# terminal B (this bootcamp repo)
bin/bootcamp stage 01      # fresh Shipyard repo at ~/shipyard-stage + baseline commit
# terminal A
cd ~/shipyard-stage && claude --model sonnet
# ... paste the prompts from PROMPTS.md ...
# terminal B
bin/bootcamp verify           # acceptance checks on ~/shipyard-stage
```

## Timing inside the part
- 3 min: topic slides
- 4 min: live demo or recorded video (deck)
- 5 min: explain and discuss
- rest: hands-on lab

## Lab
Stage part 01, start Claude Code, accept trust only after reading the folder, choose Manual mode, draft SAFETY.md with the prompt, save the settings yourself, commit the baseline.

## Evidence to show (not claims)
- `claude --version` and `/status`
- `git log --oneline -1` → baseline commit
- SAFETY.md reviewed by a human
- `/permissions` shows the saved rules

## Discussion
- Which of your daily tasks are reversible, and which are not?
- Rewrite "Update every dependency, fix whatever breaks, and deploy" as a safe delegation.
- When would you choose plan mode over auto mode?

## If it goes wrong
- Load the prepared reference: `bin/bootcamp fallback 01` (say clearly that it is prepared, not live).
- Or jump to the full reference state: `bin/bootcamp checkpoint 01 --force`.
- Play the recorded run in the deck (video `01`): Claude drafts the safety boundary from the README; the human saves the settings and commits the baseline.

## Files
- `start/` — overlay that creates the starting state (briefs, inputs)
- `solution/` — overlay that creates the reference checkpoint
- `evidence/` — captured screenshots, outputs and the recorded Claude Code run (`recorded-run/`)
