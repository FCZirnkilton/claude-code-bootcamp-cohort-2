# Best-of-N Decision Matrix

Fix the criteria and weights **before** scoring any option. Do not change them
after scoring starts. If the team wants different weights, agree and record the
change at the top of the decision document.

## Criteria (default weights)

| Criterion | Weight | 1 (poor) | 3 (adequate) | 5 (strong) |
|-----------|--------|----------|--------------|------------|
| Simplicity | x2 | Many moving parts; new concepts for the team | Familiar parts, some glue code | Smallest design that meets the brief |
| Testability | x2 | Needs real network/disk/time to test | Testable with setup or fixtures | Core logic testable in isolation with fakes |
| Security | x2 | Wide attack surface; unvalidated input reaches storage | Validation present but scattered | Single validation boundary; least privilege; no secrets in code |
| Scalability | x1 | Breaks beyond workshop scale | Handles expected load with known limits | Grows with load without redesign |
| Maintenance | x2 | Hard to change; tight coupling; extra dependencies | Changes need care across modules | Clear boundaries; stdlib or well-known deps; easy onboarding |

Maximum weighted total with default weights: 5 x (2+2+2+1+2) = **45**.

## Scoring rules

- Score every option on every criterion, each with a one-line reason.
- Show the arithmetic: `Simplicity 4x2=8, Testability 5x2=10, ...`.
- A margin under 10% of the max (under 4.5 points by default) is a close call:
  name the deciding factor explicitly.
- A hard-constraint violation (for example, "stdlib only") disqualifies an
  option whatever its score. Mark it `DISQUALIFIED: <constraint>`.

## Blank matrix

| Criterion (weight) | Option A | Option B | Option C |
|--------------------|----------|----------|----------|
| Simplicity (x2)    |          |          |          |
| Testability (x2)   |          |          |          |
| Security (x2)      |          |          |          |
| Scalability (x1)   |          |          |          |
| Maintenance (x2)   |          |          |          |
| **Weighted total** |          |          |          |

## Distinctness test (apply before scoring)

Two options are **not** distinct if they:
- share the same data model and storage, and
- differ only in naming, folder layout, or library choice for the same role.

Distinct options differ in at least one of: data model, storage, layering or
boundaries, control flow, or dependency footprint.
