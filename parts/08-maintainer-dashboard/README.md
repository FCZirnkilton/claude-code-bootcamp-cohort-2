# Part 08 · Refactor, document and create a maintainer handoff

**Project 8: Maintainer-Ready Dashboard** · 20 minutes · 13:00–13:20 (brief schedule)

## Learning goals
- Refactor with behaviour-preserving constraints
- Find duplication and unclear responsibilities; improve naming and structure
- Keep tests and browser checks as refactor guardrails
- Generate architecture notes, onboarding docs, known limitations and a handoff

## Learners leave with
- Refactored project structure
- Passing tests
- Updated README
- Architecture note
- Maintainer handoff
- Known limitations and next steps

## Run it
```sh
# terminal B (this bootcamp repo)
bin/bootcamp stage 08      # fresh Shipyard repo at ~/shipyard-stage + baseline commit
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
Run the plan prompt, cut one module from the plan, approve, implement, and compare screenshots before and after.

## Evidence to show (not claims)
- Plan approved before edits
- Tests green with unchanged assertions
- Screenshot diff before/after: only the timestamp differs
- ARCHITECTURE.md and HANDOFF.md

## Discussion
- How do you prove a refactor changed nothing?
- What belongs in a handoff that a README never says?
- Which known limitation should block the next release?

## If it goes wrong
- Load the prepared reference: `bin/bootcamp fallback 08` (say clearly that it is prepared, not live).
- Or jump to the full reference state: `bin/bootcamp checkpoint 08 --force`.
- Play the recorded run in the deck (video `08`): Plan, refactor into four modules, tests unchanged and green, pixel-identical screenshots, handoff docs.

## Files
- `start/` — overlay that creates the starting state (briefs, inputs)
- `solution/` — overlay that creates the reference checkpoint
- `evidence/` — captured screenshots, outputs and the recorded Claude Code run (`recorded-run/`)
