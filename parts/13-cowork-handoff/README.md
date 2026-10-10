# Part 13 · Claude Cowork: engineering output to stakeholder update

**Project 10B: Stakeholder Handoff** · 20 minutes · 15:25–15:45 (brief schedule)

## Learning goals
- Extend agentic work beyond code: reports, spreadsheets, presentations, documents
- Keep technical accuracy while translating risk into business impact
- Cowork permissions, local file access, reviewing browser and connector actions
- Manual, automatic and skipped approval modes

## Learners leave with
- Stakeholder-ready release update
- Risk and decision summary
- Follow-up action list
- Named owners and next steps

## Run it
```sh
# terminal B (this bootcamp repo)
bin/bootcamp stage 13      # fresh Shipyard repo at ~/shipyard-stage + baseline commit
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
Give Cowork the folder and the prompt. No Cowork? Run `/stakeholder-update` from the Skills Pack with the same inputs.

## Evidence to show (not claims)
- One page, eight sections
- Severities match the readiness report
- No invented dates
- Every connector/browser action reviewed before approval

## Discussion
- What did the update leave out on purpose?
- How do you keep severity honest in business language?
- Which approval mode would you use for Cowork in your company?

## If it goes wrong
- Load the prepared reference: `bin/bootcamp fallback 13` (say clearly that it is prepared, not live).
- Or jump to the full reference state: `bin/bootcamp checkpoint 13 --force`.
- Play the recorded run in the deck (video `13`): The readiness report becomes a one-page stakeholder update with honest severities and owners.
- Availability: Cowork needs a paid Claude plan and the Claude desktop app. Without it, run the `stakeholder-update` skill from `skills-pack/` in Claude Code with the same inputs.

## Files
- `start/` — overlay that creates the starting state (briefs, inputs)
- `solution/` — overlay that creates the reference checkpoint
- `evidence/` — captured screenshots, outputs and the recorded Claude Code run (`recorded-run/`)
