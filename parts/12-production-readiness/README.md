# Part 12 · Production readiness, security and code review

**Project 10A: Production Readiness Review** · 25 minutes · 15:00–15:25 (brief schedule)

## Learning goals
- Prototype versus production expectations
- Review dependencies, secrets, input validation, authN/authZ, permissions, errors, performance, rollback
- Use /security-review, /code-review and ultrareview (`/code-review ultra`)
- Separate verified findings from speculative concerns; prioritise by severity, effort and impact

## Learners leave with
- Security review
- Code review findings
- Top three prioritized fixes
- Named owner
- Verification plan
- Production readiness decision

## Run it
```sh
# terminal B (this bootcamp repo)
bin/bootcamp stage 12      # fresh Shipyard repo at ~/shipyard-stage + baseline commit
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
Run the review on your own project. Every High finding needs a command and its output.

## Evidence to show (not claims)
- Stored XSS proven at runtime
- Bind 0.0.0.0 + CORS * proven by the probe
- Oversized request blocks a worker
- Top 3 fixes with owners and verification
- Decision: Conditional go

## Discussion
- Which finding would you have missed without runtime evidence?
- What turns a speculative concern into a verified finding?
- Would you sign the conditional go?

## If it goes wrong
- Load the prepared reference: `bin/bootcamp fallback 12` (say clearly that it is prepared, not live).
- Or jump to the full reference state: `bin/bootcamp checkpoint 12 --force`.
- Play the recorded run in the deck (video `12`): Security review with file:line evidence, runtime proof, top three fixes and a conditional go.

## Files
- `start/` — overlay that creates the starting state (briefs, inputs)
- `solution/` — overlay that creates the reference checkpoint
- `evidence/` — captured screenshots, outputs and the recorded Claude Code run (`recorded-run/`)
