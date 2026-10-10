---
name: feature-brief
description: Turn a feature idea, issue, or vague request into a structured engineering brief with outcome, context, scope, constraints, protected areas, testable acceptance criteria, and the evidence required to prove each one. Produces the brief and a plan only; it does not write code.
when_to_use: Use when the user says "write a brief", "turn this into a spec", "plan this feature", "what should the acceptance criteria be", or is about to delegate a non-trivial change without clear scope or proof requirements.
argument-hint: "[feature idea, issue text, or path to a notes file]"
allowed-tools: Read Grep Glob Bash(git status *) Bash(git log *)
---

# Feature Brief

Convert the request below into an engineering brief a tech lead would sign off on
before any code is written.

**Request:** $ARGUMENTS

If the request is empty, ask the user for the idea in one sentence and stop.
If it is a file path, read that file and use it as the request.

## Why this exists

"Add search" is a wish. A brief states the outcome, the boundaries, and the proof.
Claude does better work against a brief, and the human can check the result
against something concrete instead of trusting a completion claim.

## Procedure

1. **Read the project context.** Read `CLAUDE.md` (and `.claude/rules/` if present).
   Note the build/test commands and any protected areas it lists.
2. **Locate the code involved.** Use Grep/Glob to find the modules the request
   touches. Record real paths only, never guessed ones.
3. **Check the working tree.** Run `git status --short` and `git log --oneline -5`
   so the brief names the baseline commit to roll back to.
4. **Find the blocking unknowns.** Ask at most three clarifying questions, and
   only for decisions that would change scope or acceptance criteria. Mark the
   rest as assumptions in the brief.
5. **Draft the brief** using the skeleton below. Every acceptance criterion must be
   observable: a command, an HTTP response, a UI state, or a file's content.
6. **Map evidence to criteria.** For each AC, name the exact command or check that
   proves it and what a pass looks like.
7. **Propose a plan** of 3-7 steps. End with an explicit "stop for review" point.
8. **Present the brief and stop.** Do not start implementing. Save it to a file
   only if the user asks (suggested path: `docs/briefs/<slug>.md`).

## Output format

```markdown
# Engineering Brief: <short title>

**Baseline:** <branch> @ <short sha> (from `git log --oneline -1`)

## Outcome
<1-2 sentences: what is true for the user when this is done>

## Context
- Relevant code: `<path>` (<what it does>)
- Conventions from CLAUDE.md: <test command, style rules>

## Scope
- In: <bullets>
- Out: <bullets, explicitly excluded work>

## Constraints
- <language/library limits, e.g. "Python 3 standard library only">
- <compatibility, performance, or data-format limits>

## Protected areas (do not modify)
- `<path or pattern>` because <reason>

## Acceptance criteria
- AC-1: <observable behaviour>
- AC-2: ...
- AC-n: Existing test suite still passes.

## Required evidence
| AC | Proof (command or check) | Pass looks like |
|----|--------------------------|-----------------|
| AC-1 | `<command>` | <expected output> |

## Plan
1. ...
n. Stop for human review before merge.

## Assumptions
- <assumption you made instead of asking>

## Open questions
- <only if still unresolved>

## Stop and ask if
- The change needs files outside Scope or inside Protected areas.
- A new dependency seems necessary.
- An acceptance criterion turns out to be untestable or contradictory.
```

## Rules

- Do not write or edit code, tests, or config while running this skill.
- Do not commit, push, or create branches.
- Do not invent file paths, commands, or existing behaviour. If you could not
  confirm something, say so under Assumptions.
- Keep acceptance criteria to what was requested. Put nice-to-haves under Out.
- Prefer 4-8 acceptance criteria. If you need more than 10, the scope is too big:
  suggest splitting it.

## Worked example (Shipyard)

Input: `/feature-brief let shipctl filter tasks by owner`

Abbreviated output:

```markdown
# Engineering Brief: Filter release tasks by owner

**Baseline:** main @ 3f2a1c9

## Outcome
`shipctl.py list --owner alice` shows only Alice's tasks.

## Scope
- In: `--owner` flag on `list`; case-insensitive match; works with `--status`.
- Out: partial-name matching, multiple owners per task.

## Constraints
- Python 3 standard library only (argparse); JSON storage format unchanged.

## Protected areas (do not modify)
- Existing task JSON fields: old data files must still load.

## Acceptance criteria
- AC-1: `list --owner alice` prints only tasks whose owner is alice (any case).
- AC-2: `list --owner alice --status pending` applies both filters.
- AC-3: An unknown owner prints "No tasks found." and exits 0.
- AC-4: `python3 -m unittest discover -s tests -q` passes, with new tests for AC-1 to AC-3.

## Required evidence
| AC | Proof | Pass looks like |
|----|-------|-----------------|
| AC-1 | `python3 shipctl.py list --owner ALICE` | only alice's rows |
| AC-4 | `python3 -m unittest discover -s tests -q` | `OK` |
```
