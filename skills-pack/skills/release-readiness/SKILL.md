---
name: release-readiness
description: Produce a Production Readiness Report for a project or component, with a concise risk summary, severity-ranked findings, evidence for each significant finding, top three fixes, recommended next-step owner, verification action, and a go / conditional go / no-go recommendation. Every important finding is tied to code, configuration, test, or runtime evidence.
when_to_use: Use when the user asks "are we ready to ship", "production readiness review", "release readiness", "go/no-go", "readiness report", or at the end of a feature before release.
argument-hint: "[project or component, e.g. notes_api, dashboard, or whole repo]"
allowed-tools: Read Grep Glob Bash(git diff *) Bash(git status *) Bash(git log *)
---

# Release Readiness

**Target:** $ARGUMENTS (default: the whole repository)

## Purpose

Prototype quality and production quality are different bars. This skill gathers
evidence across tests, security, error handling, and rollback, separates verified
findings from speculation, and ends with a decision someone can act on. The
required report sections and their order are in
[template.md](template.md). Do not drop or rename any of them.

## Procedure

1. **Baseline.** `git status --short`, `git log --oneline -5`. Note the commit
   being assessed. Uncommitted changes make the assessment provisional; say so.
2. **Test evidence.** Run `python3 -m unittest discover -s tests -q` and, if a
   dashboard exists and node is installed, `node --test dashboard/tests/*.mjs`.
   Quote the summary lines. A failing suite is a High finding.
3. **Reuse earlier evidence.** If `/change-review`, `/security-review`, or
   `/browser-verification` reports exist in this session or in `docs/`, cite them
   instead of redoing the work, and re-check anything they marked NOT VERIFIED.
4. **Review each readiness area** (one line of evidence or "not checked" each):
   - Dependencies (manifest, pinning, stdlib-only target)
   - Secrets and environment variables (no secrets in repo; config documented)
   - Input validation at every entry point
   - Authentication and authorization (needed? present? bypassable?)
   - Permission boundaries (file modes, bind address, Claude Code settings)
   - Error handling (no tracebacks to clients; atomic writes)
   - Performance and maintainability (obvious hot spots, test coverage gaps)
   - Deployment and rollback readiness (how to deploy, how to revert, tagged commit)
   For security depth, delegate to the `security-reviewer` subagent if installed.
5. **Classify findings.** Verified (exact evidence) vs Speculative (with what would
   confirm it). Only verified findings drive the decision.
6. **Rank** by severity (Critical, High, Medium, Low), then by business impact,
   then by effort (S/M/L).
7. **Choose the top three fixes:** the three changes that most reduce release risk
   per unit of effort. Each needs an owner and a verification action.
8. **Owner.** Use names the user gave you. If none, use a role (e.g. "Backend
   owner") and ask the user to confirm a person. Never invent a name.
9. **Decide** with the rules below, and report.

## Decision rules

- **No-go:** any verified Critical; any verified High without an agreed fix; or
  the test suite fails.
- **Conditional go:** verified Highs have an owner, a fix, and a verification
  action, to be completed before release; or key evidence is NOT VERIFIED but
  low-risk to obtain.
- **Go:** no open Critical or High; tests pass; runtime verified; rollback path
  exists.

## Output format

Fill [template.md](template.md) exactly. Print it in chat. Write
it to `docs/production-readiness-<target>.md` only if the user asks.

## Rules

- Every significant finding needs evidence: `path:line` with a quoted line, a
  command with its output, or a browser evidence file. No evidence, no finding;
  move it to Speculative.
- Never fabricate test results, counts, owners, dates, or metrics.
- Never print secrets; redact them.
- Read-only: no fixes, commits, tags, pushes, or deploys while running this skill.

## Worked example (Shipyard)

`/release-readiness notes_api`

- Tests: `python3 -m unittest discover -s tests -q` -> `Ran 24 tests in 0.06s` / `OK`.
- Verified High: `notes_api/server.py:41` reads `Content-Length` bytes without a cap.
- Verified Medium: `notes_api/repository.py:30` writes JSON in place (crash can
  corrupt the file); fix with temp file + `os.replace`.
- Speculative: no load test exists, so behaviour above 1k notes is unknown.
- Top three fixes: cap body size (Backend owner, S), atomic writes (Backend owner,
  S), bind server to 127.0.0.1 by default (Backend owner, S).
- Recommendation: **Conditional go**, release once fix 1 is merged and a test
  posting a 1 MB body returns 413.
