# Part 04 · Best-of-N and better engineering decisions

**Project 4: Notes API Design Tournament** · 30 minutes · 10:20–10:50 (brief schedule)

## Learning goals
- Ask for genuinely different approaches, not cosmetic variants
- Score them on a fixed matrix: simplicity, testability, security, scalability, maintenance
- Avoid the first-answer-wins trap and incoherent hybrids
- Record the chosen and rejected approaches

## Learners leave with
- Working Notes API
- Three-option decision matrix
- Selected architecture with reasoning
- Rejected Options Log

## Run it
```sh
# terminal B (this bootcamp repo)
bin/bootcamp stage 04      # fresh Shipyard repo at ~/shipyard-stage + baseline commit
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
Run the tournament prompt. Before approving, push back once: ask Claude to defend the scores of the loser it ranked second.

## Evidence to show (not claims)
- Three design files that differ in shape
- Filled matrix with totals
- Rejected Options Log with 'could become appropriate if'
- Raw test output

## Discussion
- Were the three designs genuinely different? How can you tell?
- Which criterion weight would you change for your team?
- Under what conditions would the rejected option win?

## If it goes wrong
- Load the prepared reference: `bin/bootcamp fallback 04` (say clearly that it is prepared, not live).
- Or jump to the full reference state: `bin/bootcamp checkpoint 04 --force`.
- Play the recorded run in the deck (video `04`): Three designs, the weighted matrix, the Rejected Options Log, then the approved implementation with tests.

## Files
- `start/` — overlay that creates the starting state (briefs, inputs)
- `solution/` — overlay that creates the reference checkpoint
- `evidence/` — captured screenshots, outputs and the recorded Claude Code run (`recorded-run/`)
