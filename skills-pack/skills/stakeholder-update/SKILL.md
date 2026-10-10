---
name: stakeholder-update
description: Convert engineering evidence (a production readiness report, maintainer handoff, review findings) into a one-page, business-facing stakeholder update covering release status, features completed, business impact, major risks, decisions required, top three fixes, owners and deadlines, and the recommended next step. Adds no new technical claims.
when_to_use: Use when the user explicitly runs /stakeholder-update to turn a readiness report or handoff into an update for managers, product owners, or customers. This is the fallback for the Cowork stakeholder-handoff exercise.
argument-hint: "[path(s) to readiness report and/or maintainer handoff] [optional: audience]"
disable-model-invocation: true
allowed-tools: Read Grep Glob Bash(git log *)
---

# Stakeholder Update

**Inputs:** $ARGUMENTS

If no input files are given, look for the most recent production readiness report
and maintainer handoff in this conversation or in `docs/`. If you find none, ask
the user for them and stop. Do not write an update from memory.

## Purpose

Engineers write about stack traces and test counts; stakeholders decide on dates,
scope, and risk. This skill translates without losing accuracy: every statement
in the update traces back to a line in the inputs.

## Procedure

1. **Read all inputs in full.** Note the readiness recommendation, the top three
   fixes, owners, deadlines, completed features, and risks.
2. **Identify the audience** (default: engineering manager and product owner).
   Adjust vocabulary, not facts.
3. **Translate each risk into business impact.** "Unbounded request body" becomes
   "a single malformed request can take the notes service offline". Keep the
   technical ID (e.g. PR-1) in brackets so engineers can trace it.
4. **List decisions required.** Each decision is a question with options and a
   recommendation, e.g. "Ship Friday with fix 1 only, or slip to Tuesday for
   all three? Recommend: Friday with fix 1."
5. **Owners and deadlines** come only from the inputs or the user. If missing,
   write `Owner: TBD (needs assignment)`. Never invent a name or a date.
6. **Fill [template.md](template.md)** exactly: all eight fields, in order.
7. **Check length:** one page, about 300-450 words. Cut adjectives, not facts.
8. **Traceability check.** For every sentence, confirm you can point to its source
   section. Remove anything you can't. List sources at the bottom.
9. **Present** the update in chat. Save to the path the user gives (suggested:
   `docs/stakeholder-update-<yyyy-mm-dd>.md`) only when asked.

## Output format

Use the skeleton in [template.md](template.md). The eight required fields:

1. Current release status
2. Features completed
3. Customer or business impact
4. Major risks
5. Decisions required
6. Top three fixes
7. Owners and deadlines
8. Recommended next step

## Rules

- No new findings, numbers, or estimates that are not in the inputs.
- Keep the readiness recommendation (go / conditional go / no-go) unchanged.
  Do not soften a no-go.
- No secrets, internal hostnames, credentials, or personal data.
- Plain language: define any unavoidable technical term in five words or fewer.
- Do not send, post, or email anything. Producing the text is the whole job.

## Worked example (Shipyard)

`/stakeholder-update docs/production-readiness-notes_api.md docs/handoff.md`

> **Release status:** Conditional go for Notes API v1.2 on Friday 17 Oct.
> **Features completed:** search and tagging for notes; release dashboard with
> owner filter.
> **Business impact:** release managers can find release notes by tag instead of
> scrolling; dashboard shows pending work per owner.
> **Major risks:** a single oversized request can take the service offline [PR-1].
> **Decision required:** approve Friday release conditional on fix 1? Recommend yes.
> **Top three fixes:** cap request size; crash-safe saving; local-only network access.
> **Owners and deadlines:** Backend owner (Dana, per handoff), fix 1 by Thu 16 Oct;
> fixes 2-3 TBD (needs assignment).
> **Next step:** Dana merges fix 1; QA reruns the size test Thursday; go/no-go call
> Friday 10:00.
