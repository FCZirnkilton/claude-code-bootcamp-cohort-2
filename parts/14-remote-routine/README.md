# Part 14 · Web, mobile, Remote Control and work that continues

**Project 10C: Cross-Device Continuation** · 20 minutes · 15:45–16:05 (brief schedule)

## Learning goals
- Move between terminal, desktop, web and mobile
- Continue a local session with Remote Control; monitor and steer from another device
- Local sessions versus cloud sessions; when local context or credentials are required
- Routines and scheduled work; safe automation with clear stop conditions

## Learners leave with
- Cross-device continuation checklist
- Remote verification status update
- Post-release routine brief

## Run it
```sh
# terminal B (this bootcamp repo)
bin/bootcamp stage 14      # fresh Shipyard repo at ~/shipyard-stage + baseline commit
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
Design your own post-release routine with the template; trade it with a neighbour and find one missing stop condition.

## Evidence to show (not claims)
- Session visible on claude.ai/code and the mobile app
- Steered once from the phone
- Status file written by the remote session
- Routine brief with stop conditions

## Discussion
- What must never run unattended?
- What stays local, and why?
- What is your stop condition for a routine that fails twice?

## If it goes wrong
- Load the prepared reference: `bin/bootcamp fallback 14` (say clearly that it is prepared, not live).
- Or jump to the full reference state: `bin/bootcamp checkpoint 14 --force`.
- Play the recorded run in the deck (video `14`): Verification runs, a status file is written, and a post-release routine brief with stop conditions is designed.
- Availability: Remote Control needs a claude.ai login (Team/Enterprise: enabled by an Owner). The demo runs locally; learners without access design the routine with `templates/post-release-routine-brief.md`.

## Files
- `start/` — overlay that creates the starting state (briefs, inputs)
- `solution/` — overlay that creates the reference checkpoint
- `evidence/` — captured screenshots, outputs and the recorded Claude Code run (`recorded-run/`)
