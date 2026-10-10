# Part 11 · Agent Teams: ship a feature in parallel

**Project 9C: Parallel Feature Sprint** · 30 minutes · 14:20–14:50 (brief schedule)

## Learning goals
- Choose between subagents and Agent Teams; background sessions and agent view
- Lead and teammate roles, shared task list, direct messages, plan approval
- Avoid file conflicts with explicit ownership; quality gates for parallel work
- Monitor token and coordination cost

## Learners leave with
- Parallel task plan
- Explicit role and file ownership
- Integrated feature
- Passing tests
- Team review and retrospective
- Documented coordination risks

## Run it
```sh
# terminal B (this bootcamp repo)
bin/bootcamp stage 11      # fresh Shipyard repo at ~/shipyard-stage + baseline commit
# terminal A
cd ~/shipyard-stage && claude --model sonnet
# ... paste the prompts from PROMPTS.md ...
# terminal B
bin/bootcamp verify           # acceptance checks on ~/shipyard-stage
```

## Timing inside the part
- 5 min: topic slides
- 6 min: live demo or recorded video (deck)
- 7 min: explain and discuss
- rest: hands-on lab

## Lab
Watch the instructor's team, steer one teammate, then review the integrated diff with the plugin. No access? Use the transcript, task board and checkpoint in parts/11.

## Evidence to show (not claims)
- Task list with owners and dependencies
- No file edited by two teammates
- Both suites green after integration
- `/engineering-quality:change-review` before acceptance
- Retrospective + token cost

## Discussion
- When is an Agent Team worth the extra tokens?
- What made parallel work safe here?
- What would you change in the plan approval step?

## If it goes wrong
- Load the prepared reference: `bin/bootcamp fallback 11` (say clearly that it is prepared, not live).
- Or jump to the full reference state: `bin/bootcamp checkpoint 11 --force`.
- Play the recorded run in the deck (video `11`): The team builds release notes in parallel: backend endpoint, frontend panel, tests, integrated and green.
- Availability: Agent Teams are experimental (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`). Learners without access review the recorded transcript in `evidence/recorded-run/`, the task board in the checkpoint's `docs/team-plan.md`, and the diff (`bin/bootcamp diff 11`).

## Files
- `start/` — overlay that creates the starting state (briefs, inputs)
- `solution/` — overlay that creates the reference checkpoint
- `evidence/` — captured screenshots, outputs and the recorded Claude Code run (`recorded-run/`)
