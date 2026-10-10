# Production Readiness Report: template

The report must contain these seven sections, in this order:

1. Concise risk summary
2. Severity-ranked findings
3. Evidence for each significant finding
4. Top three fixes
5. Recommended next-step owner
6. Verification action
7. Go, conditional go, or no-go recommendation

Copy the skeleton below and fill every placeholder. Write "None" rather than
deleting a section.

```markdown
# Production Readiness Report: <project / component>

**Assessed commit:** <branch> @ <short sha>   **Date:** <yyyy-mm-dd>
**Assessed by:** Claude Code (release-readiness skill), reviewed by <human name or "pending">
**Inputs:** <tests run, review reports cited, browser evidence used>

## 1. Concise risk summary
<3-5 sentences: overall risk level (Low / Medium / High), the single biggest
risk, what is solid, and what is unknown.>

## 2. Severity-ranked findings
| ID | Severity | Area | Finding | Status | Effort |
|----|----------|------|---------|--------|--------|
| PR-1 | High | Input validation | Request body size not capped | Verified | S |
| PR-2 | Medium | Error handling | Non-atomic JSON write | Verified | S |
| PR-3 | Low | Maintainability | ... | Verified | M |
| SC-1 | n/a | Performance | No load test above 1k notes | Speculative | M |

Areas: Dependencies, Secrets & environment, Input validation, Authentication,
Authorization, Permission boundaries, Error handling, Performance &
maintainability, Deployment & rollback.

## 3. Evidence for each significant finding
### PR-1
- Location: `notes_api/server.py:41`
- Evidence:
      body = self.rfile.read(int(self.headers["Content-Length"]))
- Why it matters: <impact in one or two sentences>

### Test evidence
    $ python3 -m unittest discover -s tests -q
    <verbatim summary lines>

## 4. Top three fixes
| # | Fix | Addresses | Effort | Business impact if not fixed |
|---|-----|-----------|--------|------------------------------|
| 1 | <specific change> | PR-1 | S | <impact> |
| 2 | | | | |
| 3 | | | | |

## 5. Recommended next-step owner
- Owner: <name provided by the user, or role + "to be confirmed">
- Deadline: <date provided by the user, or "to be agreed">
- Why this owner: <one line>

## 6. Verification action
- For fix 1: <test or command that proves it, e.g. "unittest posting 1 MB body expects 413">
- For fix 2: ...
- For fix 3: ...
- Release check: <final command(s) to rerun before release>

## 7. Recommendation: GO | CONDITIONAL GO | NO-GO
<2-3 sentences. For conditional go, list the exact conditions that must be met
before release and who confirms them.>

## Not verified
- <item>: <what would verify it>
```
