# Browser Verification Checklist

Use this list with the browser-verification skill, or as the manual checklist in the
fallback path. Mark each item `PASS`, `FAIL`, `N/A`, or `NOT CHECKED`, and attach
evidence to every FAIL.

## 1. Before you start

- [ ] App served locally (e.g. `python3 -m http.server 8000 --directory dashboard`)
- [ ] Backend/API running if the page depends on it
- [ ] Known starting data (fresh data file or documented seed)
- [ ] Browser window at desktop width (1280 px) to start
- [ ] Evidence folder ready: `evidence/browser/<date>/`

## 2. Core flows

For each acceptance criterion, write "user does X, expects Y" and run it.

- [ ] Page loads; title and main heading correct
- [ ] Primary navigation: every link/tab goes to the right view; back button works
- [ ] Create flow (e.g. add a release task): item appears without reload
- [ ] Read/list flow: items render with the right fields and formats (dates, owners)
- [ ] Update flow (e.g. mark complete): state changes and persists after reload
- [ ] Delete flow: item removed; confirmation if destructive
- [ ] Filter/search: results match the criteria; clearing restores the full list
- [ ] Keyboard: Tab reaches every control; Enter submits forms

## 3. States and validation

- [ ] Empty state shows a helpful message, not a blank area
- [ ] Required field empty -> clear validation message; nothing is saved
- [ ] Invalid input (bad date, very long text, `<script>` in a text field) is
      rejected or shown as plain text, never executed
- [ ] API error or offline -> visible error message, no silent failure
- [ ] Loading state (if any) appears and disappears

## 4. Console and network

- [ ] No errors on page load (copy any message verbatim)
- [ ] No errors after each flow
- [ ] No warnings that indicate bugs (failed fetches, 404 assets, CORS)
- [ ] Requests go to the expected endpoints with expected status codes

## 5. Responsive breakpoints

Check each width. Screenshot each one.

| Width | Device class | Checks |
|-------|--------------|--------|
| 375 px | Mobile | No horizontal scroll; controls reachable; text >= 14 px; tables scroll inside their container or stack |
| 768 px | Tablet | Layout adapts; no overlapping panels |
| 1280 px | Desktop | Matches wireframe; content not stretched edge to edge |

## 6. Accessibility quick pass

- [ ] Images/icons that carry meaning have alt text or labels
- [ ] Form inputs have visible labels
- [ ] Color is not the only signal for status (e.g. "Done" text plus green)
- [ ] Focus outline visible

## 7. Evidence capture

For every flow and every FAIL, capture:
- Screenshot file name: `<flow-id>-<short-desc>[-after].png`
- Console output, verbatim, with file:line when shown
- The exact steps taken (so someone else can reproduce)
- For the core flow, an optional GIF recording
- Evidence source: `chrome` (observed by Claude), `manual` (user), or `supplied`

## 8. Issue log entry

| Field | Example |
|-------|---------|
| ID | UI-3 |
| Severity | Critical / High / Medium / Low |
| Flow | F2 Filter by owner |
| Steps | Select owner "alice" in filter |
| Observed | bob's tasks still shown; console TypeError at filters.js:21 |
| Expected | Only alice's tasks |
| Evidence | evidence/browser/2026-10-10/f2-filter.png |
| Status | Open -> Fixed (verified) / Still failing / Won't fix (reason) |
