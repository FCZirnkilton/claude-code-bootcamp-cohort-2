---
name: test-debug-loop
description: Drive a bug from failing test to verified fix. Reproduce the failure, explain the likely cause before editing, add a failing regression test, make a bounded fix, rerun the relevant and full suites, and show that the regression test now passes, quoting real command output at every step.
when_to_use: Use when a test is failing, the user reports a bug or seeded defect, says "debug this", "why is this test failing", "fix this regression", or pastes a traceback or failing test output.
argument-hint: "[failing test id, error message, or bug description]"
allowed-tools: Read Grep Glob Bash(git diff *) Bash(git status *) Bash(git log *)
---

# Test-Debug Loop

**Problem:** $ARGUMENTS

If no problem was given, run the full test suite first and treat the first
failure as the problem.

## Purpose

A failing test is a debugging contract: it defines "fixed" before any code changes.
This loop stops Claude from guessing at fixes and keeps the test evidence separate
from Claude's own claim that the bug is gone.

## Test commands (Shipyard defaults; adjust to CLAUDE.md)

- Python: `python3 -m unittest discover -s tests -q`
- One Python test: `python3 -m unittest tests.test_service.ServiceTest.test_x -v`
- Dashboard: `node --test dashboard/tests/*.mjs`

## Procedure

1. **Record the baseline.** Run `git status --short` and `git log --oneline -1`.
   If there are uncommitted unrelated changes, tell the user before continuing.
   Mention that a checkpoint exists for this prompt (`/rewind` can restore code).
2. **Reproduce.** Run the narrowest command that shows the failure. Quote the
   command and the failing output verbatim (assertion, traceback, exit code).
   If it does not reproduce, stop and report what you ran and what you saw.
3. **Investigate before editing.** Read the failing test and the code under test.
   Trace the input through the code path. State one primary hypothesis and the
   line(s) you believe are wrong, plus one alternative you ruled out and why.
4. **Write the regression test first.** Add a focused test that encodes the
   correct behaviour (name it after the bug, e.g. `test_update_keeps_tags`). Run
   it and quote the output showing it **fails for the expected reason**. If it
   fails for a different reason, fix the test, not the code.
5. **Make a bounded fix.** Change the smallest amount of code, only in the files
   your diagnosis named. No refactors, renames, or formatting changes.
6. **Verify the fix.** Run the regression test (quote: it now passes), then the
   whole relevant suite (quote the summary line).
7. **Check for collateral damage.** Run the other suite if the fix touched shared
   code. Run `git diff --stat` and confirm only the expected files changed.
8. **Hand over to review.** Produce the debug report below and recommend running
   `/change-review` to complete the Review Before Merge checklist.

## If an approach fails

- After a failed attempt, do not stack a second patch on top of the first. Explain
  what the failure taught you and recommend the user `/rewind` and choose
  **Restore code** (keeps the conversation, restores files edited by Claude).
  `/rewind` does not undo changes made through Bash (`rm`, `mv`, `cp`).
- After **three** failed fix attempts, stop and report. Do not keep trying.

## Pairing with /goal

For a measurable completion condition, suggest the user set, for example:
`/goal python3 -m unittest discover -s tests -q exits 0 and test_update_keeps_tags passes`.
The goal evaluator only reads the transcript, so always print the test output.

## Output format

```markdown
# Debug Report: <bug in one line>

## Reproduction
    $ <command>
    <failing output, verbatim>

## Diagnosis
- Cause: <what is wrong> at `<path>:<line>`
- Why: <how the input reaches the bug>
- Ruled out: <alternative hypothesis and evidence>

## Regression test
- Added `<test id>` in `<path>`
- Before fix:
      $ <command>
      <FAIL output>

## Fix
- `<path>:<lines>`: <one-line description> (diff: +X / -Y)

## Verification
    $ <regression test command>
    <passing output>
    $ <full suite command>
    <summary line, e.g. "Ran 19 tests in 0.05s" / "OK">

## Files changed
<`git diff --stat` output>

## Next step
Run `/change-review` before merge. Remaining risks: <list or "none known">.
```

## Rules

- Never delete, skip, or loosen a test to make the suite pass. Change a test's
  expected value only if the test is demonstrably wrong; say so and get agreement.
- Never claim a test passed without showing the output from this session.
- No commits, pushes, or branch changes. No new dependencies.
- Keep the fix inside the files named in the diagnosis; ask before widening scope.

## Worked example (Shipyard Notes API, seeded defect)

`/test-debug-loop updating a note drops its tags`

1. Reproduce: `python3 -m unittest tests.test_service -v` ->
   `FAIL: test_update_note ... AssertionError: [] != ['release']`.
2. Diagnosis: `notes_api/service.py:58` builds the updated note from
   the request fields only, so `tags` defaults to `[]` when the client omits it.
   Ruled out: the repository's JSON write, because the raw file shows tags present
   before the update.
3. Regression test `test_update_without_tags_keeps_existing_tags` fails with the
   same assertion.
4. Fix: merge the existing note's fields before applying updates (+3 / -1).
5. Regression test passes; full suite `Ran 19 tests` / `OK`; `git diff --stat`
   shows `notes_api/service.py` and `tests/test_partial_update.py` only.
