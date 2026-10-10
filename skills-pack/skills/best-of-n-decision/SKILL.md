---
name: best-of-n-decision
description: Generate N genuinely different approaches to an engineering decision, score them against a fixed decision matrix (simplicity, testability, security, scalability, maintenance), recommend one, and write a Rejected Options Log for every option not chosen. Stops before implementation.
when_to_use: Use when the user asks to "compare approaches", "give me options", "best-of-n", "design tournament", "which design should we use", or before committing to an architecture, storage, or API design.
argument-hint: "[decision to make] [optional: number of options, default 3]"
allowed-tools: Read Grep Glob Bash(git status *) Bash(git log *)
---

# Best-of-N Decision

**Decision to make:** $ARGUMENTS

Default to **3** options unless the arguments ask for a different number (max 5).
If no decision is given, ask for one and stop.

## Why this exists

The first plausible design tends to win by default. Best-of-N makes Claude produce
real alternatives, compare them on criteria fixed *before* scoring, and record
why the losers lost, so the choice can be revisited when conditions change.

## Procedure

1. **Frame the decision.** Restate the problem, the constraints (read `CLAUDE.md`),
   and what "good" means for this project in 3-5 bullets.
2. **Fix the matrix first.** Use the criteria and weights in
   [decision-matrix.md](decision-matrix.md). If the user wants different weights,
   agree on them now, before any option is scored.
3. **Generate N options that differ structurally.** Each option must differ from
   the others in at least one of: data model, storage, layering/boundaries,
   control flow (sync/async, push/pull), or dependency footprint.
   Apply the distinctness test: if two options would share most of their code,
   they are one option. Replace the duplicate.
4. **Describe each option** in the same shape: summary, key components (real
   module/file names for this repo), what a test for it looks like, main risk.
5. **Score** each option 1-5 per criterion with a one-line justification per
   score. Compute the weighted total. Show your arithmetic.
6. **Sanity-check the winner.** Does it violate a hard constraint? Is the margin
   under 10%? If so, say the result is close and name the deciding factor.
7. **Hybrids.** You may borrow one idea from a losing option only if it does not
   add a second paradigm (for example, two storage layers or two error models).
   Name the borrowed idea explicitly; otherwise do not mix.
8. **Write the Rejected Options Log** for every option not chosen, using
   [rejected-options-log.md](rejected-options-log.md). All five fields are required.
9. **Stop.** Present the result and ask the human to approve the choice before any
   implementation. Save to `docs/decisions/<slug>.md` only if asked.

## Output format

```markdown
# Decision: <title>

## Problem and constraints
- ...

## Options
### Option A: <name>
- Summary:
- Key components:
- How it is tested:
- Main risk:
### Option B: <name>
...

## Decision matrix
| Criterion (weight) | A | B | C |
|--------------------|---|---|---|
| Simplicity (x2)    | 4 - <why> | ... | ... |
| Testability (x2)   | ... |
| Security (x2)      | ... |
| Scalability (x1)   | ... |
| Maintenance (x2)   | ... |
| **Weighted total** | **nn** | **nn** | **nn** |

## Selected: Option <X>
<3-5 sentences of reasoning, including the deciding factor and any borrowed idea>

## Rejected Options Log
<one block per rejected option, per rejected-options-log.md>

## Next step
Awaiting approval. On approval, implement Option <X> starting with <first step>.
```

## Rules

- Do not implement any option while running this skill. No file edits, no commits.
- No cosmetic variants (same design, different names or folder layout).
- Do not change criteria or weights after scoring has started.
- Scores need a reason. "4" with no justification is not acceptable.
- Do not claim performance numbers you did not measure. Write "estimated".

## Worked example (Shipyard Notes API)

`/best-of-n-decision storage and layering for the Notes API`

- **A: Layered in-memory + JSON file.** `repository.py` (dict + atomic JSON
  write), `service.py` (validation), `server.py` (`http.server` handler).
- **B: SQLite via `sqlite3`.** Repository wraps SQL; service unchanged; schema
  migration on start.
- **C: Single-module handler.** Request handler reads/writes the JSON file
  directly; no service layer.

Matrix result (weights 2/2/2/1/2): A = 36, B = 34, C = 27. **Selected: A.** It is
stdlib-only, easy to test by swapping the repository for an in-memory fake, and
adequate for workshop scale. Rejected Options Log for B records "Reconsider when
notes exceed ~10k or concurrent writers appear". C is rejected because the
untestable handler mixes I/O and validation.
