# Scoring Rubric (Capstone and Reflection)

> **For graders.** Score only what the submission shows. A claim without an artifact scores as if the work is absent. Work through it in this order:
>
> 1. Run the **automatic-fail screen**.
> 2. Rerun the tests.
> 3. Score the capstone (50 points).
> 4. Score the reflection (20 points).
> 5. Check the passing gates.
> 6. Record everything in `grading-sheet.csv`.
>
> Use whole points. When a submission falls between two bands, choose the lower band and write one sentence explaining why in `notes`.

## Step 1: Automatic-fail screen

Complete this screen before scoring. Any confirmed item fails the assessment. Record the evidence (file, line, commit, screenshot), and have a second grader confirm before you release the result.

| Condition | How to check | Confirmed if |
|---|---|---|
| **Exposed credentials** | The secret-scan commands below, plus a visual check of every screenshot and log in `capstone/evidence/` | A real, usable credential appears anywhere in the submission, including history and images. Obvious placeholders (`TOKEN=changeme`, `sk-EXAMPLE`) are not a fail; note them |
| **Fabricated test results** | See "Detecting fabricated results" below | Submitted output could not have been produced by the submitted code, or the learner cannot or will not produce the raw output when asked |
| **Unsafe irreversible actions** | Look in the reflection, the transcript excerpts, `git reflog` (if a repository was provided), the permission boundary, and the settings | A force-push or history rewrite on a shared branch, deletion of data outside the project, `bypassPermissions` on the host, disabled hooks or deny rules used to get past a block, or a deploy or external message sent without approval |

Secret-scan commands (run them in the submitted repository):

```bash
git log -p --all | grep -inE "api[_-]?key|token|secret|password|BEGIN .*PRIVATE KEY|ghp_|sk-"
git log --all --stat -- .env '*.env' '*.pem'
grep -rinE "api[_-]?key|token|secret|password" capstone/
```

**Not automatic fails:**
- Failing tests reported honestly.
- An incomplete feature that is documented as incomplete.
- `git reset --hard` on the learner's own unpushed feature branch, when it was done by the learner as a deliberate recovery step.
- Placeholder secrets.

### Detecting fabricated results

1. **Ask for the command and raw output.** `capstone/evidence/tests.txt` must contain the exact command, the unedited output, and the exit code. Summaries ("31 tests passed") are not evidence.
2. **Rerun it.** Check out the submitted commit and run the exact command, for example `python3 -m unittest discover -s tests -v; echo "exit=$?"`. Compare the result with the submission:
   - The test count matches.
   - The test names match the test files.
   - Each status (ok, FAIL, ERROR) matches.
3. **Check consistency.** Every test name in the output must exist in the code (`grep -rn "def test_" tests/`). The output must match the real `unittest` format (`Ran N tests in X.XXXs`, then `OK` or `FAILED (failures=N)`). Warning signs:
   - Round or identical timings across runs.
   - A missing `Ran` line.
   - Tests listed that do not exist.
   - A pass count higher than the number of test methods.
4. **Check the red run** (for bug-style changes, or where one is claimed). Check out the parent commit, or revert the fix locally, and confirm that the regression test actually fails.
5. **Check runtime evidence against the code.** The `curl` responses must match the code's real formats: status codes, header names, and the error JSON shape. Screenshots must show UI that exists in the submitted code, at the stated widths.
6. **If the rerun does not match**, first rule out environment differences such as the Python version or OS. Then ask the learner for a fresh raw run, with a 48-hour deadline. A plausible environment difference, explained, is not fabrication. Output that cannot be reproduced and is not explained is fabrication.

## Step 2: Capstone (50 points)

| Criterion | Pts | Full marks | Partial | Minimal / zero | Evidence to look at |
|---|---|---|---|---|---|
| **Scope and brief** | 7 | 6-7: The brief has an outcome, constraints, protected areas, testable acceptance criteria, and required evidence. The plan was reviewed and at least one change requested or explicitly approved. The change stays inside the brief | 3-5: The brief is present, but the acceptance criteria are vague or untestable, or the change has minor drift outside scope that is acknowledged | 0-2: No brief, or a one-line prompt; unacknowledged scope creep | `brief.md`, `git diff --stat`, D11 mapping |
| **Diff quality** | 8 | 7-8: Focused commits with clear messages. Every material line is explainable. Follows project conventions (layering, stdlib only, `textContent`). No dead code or unrelated reformatting | 4-6: Works, but has noise (unrelated edits, a large single commit, minor convention breaks) | 0-3: Unreviewed dump, unexplained changes, new dependencies, or existing tests weakened | `capstone.diff`, `git log`, Review Before Merge row 2 |
| **Tests** | 10 | 9-10: New tests cover every acceptance criterion and the important edge cases (empty, boundary, invalid). Tests are deterministic and isolated (temp DB, injected clock or date). They pass on rerun. A red run is shown where relevant | 5-8: Tests pass but miss edge cases or one acceptance criterion; some are shallow (assert only the status code) | 0-4: Tests are trivial, missing, failing without explanation, or do not run | `tests/`, `evidence/tests.txt`, grader rerun |
| **Verification evidence** | 10 | 9-10: Runtime or browser evidence demonstrates each user-visible acceptance criterion. For UI: flows, console, three breakpoints, and an issue log with before and after. For API: an exact `curl -i` transcript, including error paths | 5-8: Evidence covers the happy path only, or is partly missing (for example, no error path or breakpoints) | 0-4: No real-interface verification, or only Claude's description of it | `evidence/runtime/`, Review Before Merge row 5 |
| **Production Readiness Report** | 10 | 9-10: All seven sections present. Findings are severity-ranked under the defined scale. Every Medium-or-above finding has evidence. Speculative items are separated. The top three fixes are justified. There is a named owner, a concrete verification action, and a go, conditional go, or no-go decision consistent with the findings | 5-8: All sections present, but evidence is thin, severities are inconsistent, or the recommendation is weakly connected to the findings | 0-4: Sections missing, findings unsupported, or a "go" that contradicts the evidence | `production-readiness-report.md` |
| **Safety and recovery** | 5 | 5: A written permission boundary, a recovery point made before autonomous work (hash recorded), feature branch or worktree, and a Review Before Merge security row with evidence | 3-4: Boundary or recovery point present but incomplete (for example, no hash, or a vague boundary) | 0-2: Worked on `main` with no recovery point and no boundary | `permission-boundary.md`, `git log`, Review Before Merge rows 4 and 6 |

**Readiness gate (pass/fail, separate from the points).** The report must contain a **risk summary**, **top three fixes**, a **named owner**, and a **verification step**. If any one is missing, record `gate_readiness_elements = N`.

## Step 3: Reflection (20 points)

| Criterion | Pts | Full marks | Partial | Minimal / zero |
|---|---|---|---|---|
| **Rejected approach** | 7 | 6-7: A real alternative, with its advantages, the primary reason it was rejected (tied to a criterion or evidence), and the conditions under which it would fit. If it was tried, the recovery method is described | 3-5: An alternative is named, but the reasoning is generic, or there are no "appropriate later" conditions | 0-2: No real alternative, or a cosmetic variant presented as an alternative |
| **Human checkpoint** | 7 | 6-7: A specific moment, what was checked, the evidence cited, the decision and its consequence, and a lesson about where to place or enforce the checkpoint | 3-5: A moment is described, but without evidence or without reflection on placement | 0-2: Generic ("I reviewed the code") or no checkpoint |
| **Unresolved risk** | 6 | 5-6: A concrete residual risk with likelihood and impact, evidence or the reason it cannot be verified, an owner, and a verification action. It is consistent with the readiness report | 3-4: A risk is named, but no owner or verification action, or it is inconsistent with the report | 0-2: "No risks", or a vague statement |

## Step 4: Totals and passing gates

```
quiz_points       = quiz_correct_of_25 x 1.2            (max 30)
capstone_total    = sum of the six capstone criteria    (max 50)
reflection_total  = sum of the three reflection criteria (max 20)
overall_total     = quiz_points + capstone_total + reflection_total (max 100)
```

| Gate | Rule |
|---|---|
| Overall | `overall_total >= 70` |
| Capstone | `capstone_total >= 30` (60%) |
| Genuine evidence | The grader's rerun or check confirms that the test or runtime evidence is real (Y/N) |
| Readiness elements | Risk summary, top three fixes, named owner, and verification step all present (Y/N) |
| Automatic fail | None of credentials, fabrication, or unsafe irreversible action confirmed |

**PASS** only if every gate is met. Otherwise **FAIL**, and the `notes` column names the gate or gates that failed.

`grading-sheet.csv` includes a `MAX` row and an example row with spreadsheet formulas. Copy the example row for each learner. If you fill the sheet by hand, compute the totals with the formulas above.

## Grader notes

- **Score against the learner's approved brief.** A justified change to an acceptance criterion is acceptable. A silent change counts as scope drift.
- **Honest negative evidence is good evidence.** "AC4 fails at 375 px; logged as UI-3, owner assigned" can still earn most of the verification points.
- **Claude-written prose is allowed.** Unverified Claude claims are not. If the report says "no SQL injection", look for the evidence that backs it.
- **Watch for "evidence" that is just Claude's summary of a run.** Ask: where is the raw output?
- **Feedback.** Write one strength and one improvement per component in `notes`.
- **Conflict of interest or uncertainty about an automatic fail.** Escalate to the instructor. Never release an automatic-fail result without a second grader.
