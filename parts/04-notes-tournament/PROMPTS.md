# Part 04 prompts

Copy each block into Claude Code in order. Read the output before sending the next one.

## 1. Tournament (no code)

```text
Read briefs/notes-api.md. Follow the tournament rules exactly: write three genuinely different designs to designs/option-a-*.md, option-b-*.md and option-c-*.md, score them in decision/decision-matrix.md with the fixed weighted criteria, recommend a winner, and write decision/rejected-options-log.md with every required field. Do not write any implementation code. Stop and wait for my approval.
```

## 2. Implement the approved design

```text
I approve your recommended design. Implement it in notes_api/ with end-to-end tests in tests/test_notes_api.py that run a real server on an ephemeral port. Run the full test suite and show the raw output. Do not commit.
```
