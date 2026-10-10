# Stakeholder Update template

One page. Eight fields, in this order. Every statement must trace back to the
readiness report, handoff, or the user. Write `TBD (needs assignment)` instead
of inventing an owner or deadline.

```markdown
# Release Update: <product / component> <version>

**Date:** <yyyy-mm-dd>   **Prepared for:** <audience>   **Prepared from:** <input documents>

## 1. Current release status
<One line: GO / CONDITIONAL GO / NO-GO, target date, and the condition if any.>

## 2. Features completed
- <feature, in user terms>
- <feature>

## 3. Customer or business impact
- <who benefits and how, in one line each>
- <what customers will notice, including any limitation>

## 4. Major risks
| Risk (plain language) | Business impact | Likelihood | Ref |
|-----------------------|-----------------|------------|-----|
| <e.g. one oversized request can stop the service> | <e.g. notes unavailable until restart> | <Low/Med/High> | PR-1 |

## 5. Decisions required
1. <Question?> Options: <A> / <B>. **Recommendation:** <A>, because <reason>.
   Needed by: <date or TBD>.

## 6. Top three fixes
1. <fix in plain language> [PR-1]
2. <fix> [PR-2]
3. <fix> [PR-3]

## 7. Owners and deadlines
| Action | Owner | Deadline |
|--------|-------|----------|
| <fix 1> | <name from inputs or TBD (needs assignment)> | <date or TBD> |
| <fix 2> | | |
| <fix 3> | | |
| Go/no-go decision | <name> | <date> |

## 8. Recommended next step
<One or two sentences: the single next action, who does it, and when.>

---
Sources: <document name, section> for each field above.
```

## Translation guide

| Engineering phrase | Stakeholder phrase |
|--------------------|--------------------|
| Unbounded request body / DoS | One bad request can take the service offline |
| Non-atomic write | A crash while saving could corrupt stored notes |
| Missing input validation | The system accepts bad data that can break pages |
| Tests pass (24/24) | Automated checks pass |
| NOT VERIFIED in browser | Not yet checked in a real browser |
| Conditional go | Ready to release once <condition> is done |
