# Part 05 · Testing, debugging, checkpoints and /goal

**Project 5: Resilient Notes API** · 30 minutes · 10:50–11:20 (brief schedule)

## Learning goals
- Generate meaningful tests and find missing edge cases
- Use a failing test as the debugging contract; investigate before editing
- Use checkpoints: /rewind → restore code without losing the conversation
- Use /goal for a measurable completion condition
- Separate test evidence from Claude's own completion claim

## Learners leave with
- Expanded test suite
- Documented diagnosis
- Verified bug fix
- Successful checkpoint restore
- Completed Review Before Merge checklist

## Run it
```sh
# terminal B (this bootcamp repo)
bin/bootcamp stage 05      # fresh Shipyard repo at ~/shipyard-stage + baseline commit
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
Try the deliberately heavy approach first (rewrite the repository update), then /rewind → Restore code, and apply the bounded fix.

## Evidence to show (not claims)
- Failing test output before the fix
- One-line diff in service.py
- Passing full suite
- /rewind restore of the deliberately bad attempt
- Seven-point checklist with evidence

## Discussion
- Why write the failing test before reading the code?
- What does /rewind restore, and what does it not restore?
- What makes a /goal condition checkable from the transcript?

## If it goes wrong
- Load the prepared reference: `bin/bootcamp fallback 05` (say clearly that it is prepared, not live).
- Or jump to the full reference state: `bin/bootcamp checkpoint 05 --force`.
- Play the recorded run in the deck (video `05`): Failing regression test, diagnosis to the exact line, /goal-driven fix, green suite and the completed checklist.

## Files
- `start/` — overlay that creates the starting state (briefs, inputs)
- `solution/` — overlay that creates the reference checkpoint
- `evidence/` — captured screenshots, outputs and the recorded Claude Code run (`recorded-run/`)
