# Practical Capstone

**Weight:** 50% of the assessment (50 points). **Pass gate:** at least 30/50.
**Expected effort:** 2 to 3 hours. **Due:** see the timeline in [`README.md`](README.md).

## The task

Take Shipyard from your end-of-workshop checkpoint, or from the supplied Project 10 checkpoint, and ship **one bounded change** the way you practiced it in the workshop:

1. Brief
2. Plan
3. Implement
4. Test
5. Verify
6. Review
7. Make a readiness decision

You are the engineer of record. Claude Code does the engineering work; you set the boundaries, check the evidence, and make the decisions.

What is graded is the **quality of your evidence and decisions**, not the size of the feature. A small change with genuine evidence scores higher than a large change with claims.

## Choose one option

### Option 1: Export notes as Markdown (Notes API)

Add `GET /api/notes/export` that returns all notes as one Markdown document.

| # | Acceptance criterion |
|---|---|
| AC1 | The response has status 200, `Content-Type: text/markdown; charset=utf-8`, and a `Content-Disposition` header suggesting `notes.md` |
| AC2 | Each note is rendered as `## <title>`, followed by its tags (if any) and its body. Notes are ordered by `created_at` |
| AC3 | Titles or bodies that contain Markdown control characters or HTML cannot break the document structure, for example a title that starts with `#` or contains a newline |
| AC4 | With no notes, the endpoint returns a valid document with a "No notes" line, not an error |
| AC5 | Existing endpoints and tests are unchanged |

- Protected: `notes_api/repository.py` schema; all existing routes.
- Runtime evidence: a `curl -i` transcript.

### Option 2: Overdue-task badge on the dashboard

Show a badge with the number of overdue release tasks (status pending, due date before today) on the release dashboard, and add a way to filter the task list to overdue tasks.

| # | Acceptance criterion |
|---|---|
| AC1 | The badge shows the correct count for a seeded data set that has 0, 1, and several overdue tasks. It is hidden or shows "0" according to your brief |
| AC2 | Tasks that are due **today** are not overdue. Done tasks are never overdue. Tasks with no due date are never overdue |
| AC3 | Clicking the badge filters the list to overdue tasks. Clicking again clears the filter |
| AC4 | The count updates without a reload when a task is marked done |
| AC5 | There are no console errors, and the layout works at 375, 768, and 1280 px |

- Protected: the API contract (no backend changes unless your brief justifies them); other components.
- Runtime evidence: Claude in Chrome evidence or the manual [browser verification checklist](../templates/browser-verification-checklist.md), with screenshots.
- The overdue rule must live in a function that can be unit-tested. Pass the date in as a parameter so the tests are deterministic.

### Option 3: Rate limit on the Notes API

Limit write requests (POST, PATCH, DELETE) per client IP.

| # | Acceptance criterion |
|---|---|
| AC1 | With a limit of N writes per 60 seconds per client (default N=30, configurable through an environment variable), request N+1 within the window returns 429 with a `Retry-After` header and a JSON `{"error": ...}` body |
| AC2 | GET requests and `/api/health` are not limited |
| AC3 | Once the window has passed, writes are accepted again |
| AC4 | The limiter is thread-safe under `ThreadingHTTPServer` |
| AC5 | Tests are deterministic: they use an injectable clock, with no `sleep` calls of more than about 0.1 seconds |

- Protected: the service and repository layers; existing routes and responses.
- Runtime evidence: a shell loop of `curl` requests showing the 201 responses, then 429, then recovery.

Do not choose an option that requires third-party packages. All options must stay **Python 3 stdlib plus vanilla HTML/JS**. You may adjust an acceptance criterion in your brief if you justify the change; graders score against your approved brief.

## Rules

- Work on a feature branch or a worktree. Make the recovery point **before** any autonomous work, and record its hash.
- Work under a written permission boundary. Do not use `bypassPermissions` on your host machine.
- Use synthetic data only. Do not use real names, emails, or credentials.
- Never weaken, skip, or delete existing tests to make your change pass.
- Keep raw evidence. Paste command output exactly as it was produced, without trimming the lines that matter (the command, `Ran N tests`, `OK`/`FAILED`, and the exit code).
- If something does not work, say so. Honest, documented failure is graded on its merits. Fabricated success is an automatic fail.

## Exact deliverables

Put everything in a `capstone/` folder in your repository (or archive), using these names:

| # | Deliverable | File / location | Template |
|---|---|---|---|
| D1 | Engineering brief, including the plan Claude proposed and the changes you requested | `capstone/brief.md` | [engineering-brief](../templates/engineering-brief.md) |
| D2 | Permission boundary and recovery point | `capstone/permission-boundary.md` | [permission-boundary](../templates/permission-boundary.md) |
| D3 | Working change on a branch with focused commits | branch name in `capstone/brief.md` | n/a |
| D4 | Reviewed diff | `capstone/capstone.diff` (`git diff <base>...<branch>`) | n/a |
| D5 | Tests: new tests covering the acceptance criteria and edge cases | `tests/` in the repository | n/a |
| D6 | Test evidence: the command, raw output, and exit code. For a bug-style change, also show a red run before the fix | `capstone/evidence/tests.txt` | n/a |
| D7 | Runtime or browser verification evidence | `capstone/evidence/runtime/` (curl transcript, or screenshots plus the issue log) | [browser-verification-checklist](../templates/browser-verification-checklist.md) |
| D8 | Review Before Merge checklist, with evidence for all seven points | `capstone/review-before-merge.md` | [review-before-merge-checklist](../templates/review-before-merge-checklist.md) |
| D9 | Production Readiness Report with all seven required sections | `capstone/production-readiness-report.md` | [production-readiness-report](../templates/production-readiness-report.md) |
| D10 | Engineering reflection (graded separately, 20 points) | `capstone/reflection.md` | [reflection-template](reflection-template.md) |
| D11 | Mapping from each acceptance criterion to its test name and evidence file | a table at the end of `capstone/brief.md` | n/a |

**Required in D9:** a risk summary, top three fixes, named owner, and verification step. If any of these is missing, the submission fails the passing criteria whatever the score.

**Before you submit:**
- Run `git log -p | grep -inE "api[_-]?key|token|secret|password|BEGIN .*PRIVATE KEY"` on your branch and review every match.
- Check that `.env` and any `*.db` files are not committed.
- Check every screenshot for tokens or personal data.

## How it is graded

See [`rubric.md`](rubric.md). In summary:

| Area | Points |
|---|---|
| Scope and brief | 7 |
| Diff quality | 8 |
| Tests | 10 |
| Verification evidence | 10 |
| Production Readiness Report | 10 |
| Safety and recovery | 5 |
| **Total** | **50** |

Graders rerun your test command on your submitted commit. They may also ask for the raw output of any command you cite.
