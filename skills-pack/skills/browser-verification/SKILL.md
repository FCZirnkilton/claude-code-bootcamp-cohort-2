---
name: browser-verification
description: Verify a web feature in a real browser with Claude in Chrome. Exercise the core user flows, read console errors, check responsive breakpoints, capture screenshot evidence, log issues with before-and-after status, and turn findings into focused fixes. Includes a manual fallback when Chrome integration is unavailable.
when_to_use: Use when the user says "verify in the browser", "check it in Chrome", "test the dashboard UI", "does the page work", "check for console errors", "check mobile layout", or after a UI change and before marking it done.
argument-hint: "[URL or page] [flow to verify, e.g. 'add a release task and filter by owner']"
---

# Browser Verification

**Target and flow:** $ARGUMENTS

If no URL is given, use the project's dashboard (see Setup). If no flow is given,
derive the flows from the acceptance criteria in this conversation or the README.

## Purpose

Unit tests don't show a broken layout, a swallowed click handler, or a console
error. This skill gathers real browser evidence so the Runtime point of the Review
Before Merge checklist can be PASS. Use [checklist.md](checklist.md) for the full
list of checks.

## Setup

1. **Check Chrome access.** Claude in Chrome needs `claude --chrome` (or `/chrome`
   enabled), the Claude in Chrome extension, and a claude.ai paid-plan login. It
   is not supported in WSL. If browser tools are unavailable, use the
   **Fallback** section below. Do not pretend to have browsed.
2. **Serve the app.** For Shipyard's static dashboard, ask the user to start (or
   run in the background with permission):
   `python3 -m http.server 8000 --directory dashboard` and open
   `http://localhost:8000/`. If the dashboard reads the Notes API, the API server
   must be running too.
3. **Prepare an evidence folder:** `evidence/browser/<yyyy-mm-dd>/`. Ask before
   creating it if the repo doesn't already have an `evidence/` convention.

## Procedure

1. **List the flows** to verify (3-6), each as "user does X, expects Y".
2. **Load the page.** Record the URL and page title. Read the console. Copy any
   errors or warnings verbatim.
3. **Run each flow** step by step: click, type, submit. After each flow, record
   the observed result, read the console again, and take a screenshot.
4. **Check states:** empty state, a validation error (submit an invalid form),
   loading or error state if the app has one.
5. **Check responsive layout** at 375 px (mobile), 768 px (tablet), and 1280 px
   (desktop). Look for horizontal scroll, overlapping or cut-off elements, and
   unreadable text. Screenshot each width.
6. **Log issues** in the issue log (format below), one row per distinct problem,
   with severity and the evidence file.
7. **Propose focused fixes.** For each issue, name the likely file and change.
   Fix only if the user asks, one issue at a time.
8. **Re-verify after fixes.** Repeat the affected flow, update the issue's status
   to `Fixed (verified)` with new evidence, or `Still failing`.

## Fallback (no Chrome integration)

Use the captured evidence supplied with the workshop (screenshots, console logs)
or ask the user to perform each step and paste what they see. Fill the same
report, mark every evidence item `source: manual` or `source: supplied`, and
never mark a check as observed by Claude when it was not.

## Output format

```markdown
# Browser Verification: <page / feature>

**URL:** http://localhost:8000/  **Date:** <yyyy-mm-dd>  **Method:** Claude in Chrome | manual fallback

## Flows
| # | Flow | Expected | Observed | Result | Evidence |
|---|------|----------|----------|--------|----------|
| F1 | Add task "Tag v1.2" for alice | Row appears in Pending | Row appears | PASS | evidence/browser/.../f1.png |

## Console
- Page load: <"no errors" or verbatim messages>
- After F2: `Uncaught TypeError: ... (app.js:88)`

## Responsive
| Width | Result | Notes | Evidence |
|-------|--------|-------|----------|
| 375 px | FAIL | table overflows horizontally | .../375.png |

## Issue log
| ID | Severity | Flow | Observed | Expected | Evidence | Status (before -> after) |
|----|----------|------|----------|----------|----------|--------------------------|
| UI-1 | High | F2 | Filter ignores owner | Only alice's rows | f2.png, console | Open -> Fixed (verified) |

## Recommended fixes
1. UI-1: `dashboard/filters.js`: <specific change>
```

## Rules

- Never describe a page you did not load, or console output you did not read.
- Do not enter real credentials, log in to accounts, or submit forms to production
  systems. Pause and hand over to the user at logins, CAPTCHAs, and JS `alert`
  or `confirm` dialogs.
- Stay on the target origin unless the flow requires otherwise.
- No commits or pushes. Fixes only on request.

## Worked example (Shipyard dashboard)

`/browser-verification http://localhost:8000/ filter release tasks by owner`

Claude loads the page (console clean), adds a task for `alice`, selects owner
filter "alice", and sees bob's tasks still listed. The console shows
`Uncaught TypeError: Cannot read properties of undefined (reading 'toLowerCase') at filters.js:21`.
Logged as UI-1 (High) with `f2-filter.png`. At 375 px the task table forces
horizontal scroll (UI-2, Medium). After the user approves a fix that guards the missing
owner field, Claude repeats F2: only alice's rows show, console clean, and UI-1
becomes `Open -> Fixed (verified)` with `f2-filter-after.png`.
