# Part 02 · Prompting Claude Code like a tech lead

**Project 2: CLI Release Task Manager** · 25 minutes · 09:20–09:45 (brief schedule)

## Learning goals
- Replace small prompts with a complete engineering brief
- State outcome, context, constraints, protected areas and acceptance criteria
- Require proof instead of accepting completion claims
- Ask for a plan first; review and challenge it; intervene only at decision points

## Learners leave with
- Working CLI application (`shipctl.py`)
- Structured engineering brief
- Test suite
- Acceptance evidence table
- README with usage examples

## Run it
```sh
# terminal B (this bootcamp repo)
bin/bootcamp stage 02      # fresh Shipyard repo at ~/shipyard-stage + baseline commit
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
Run the two prompts. Reject the first plan once with a concrete objection (for example: atomic writes). Check the evidence table against the brief yourself.

## Evidence to show (not claims)
- The approved plan
- Raw `unittest -v` output
- AC → test table
- Real CLI session for AC1, AC4, AC5

## Discussion
- Which acceptance criterion was the hardest to prove, and why?
- What would you have challenged in the plan?
- What is the difference between "tests pass" and "here is the command and its output"?

## If it goes wrong
- Load the prepared reference: `bin/bootcamp fallback 02` (say clearly that it is prepared, not live).
- Or jump to the full reference state: `bin/bootcamp checkpoint 02 --force`.
- Play the recorded run in the deck (video `02`): Plan mode proposal, approval, implementation, 15 passing tests and the AC evidence table.

## Files
- `start/` — overlay that creates the starting state (briefs, inputs)
- `solution/` — overlay that creates the reference checkpoint
- `evidence/` — captured screenshots, outputs and the recorded Claude Code run (`recorded-run/`)
