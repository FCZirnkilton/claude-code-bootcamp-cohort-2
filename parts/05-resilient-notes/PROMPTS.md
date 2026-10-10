# Part 05 prompts

Copy each block into Claude Code in order. Read the output before sending the next one.

## 1. Investigate before editing

```text
Read BUG-REPORT.md. Do not change any code yet. Reproduce BUG-101 with a failing regression test in tests/test_partial_update.py (title-only PATCH must keep the body; also cover body-only, explicit empty body and empty patch). Run it and show the failure. Then explain the most likely cause with file and line.
```

## 2. Measurable completion with /goal

```text
/goal BUG-101 is fixed with the smallest change in notes_api/service.py, python3 -m unittest discover -s tests -q exits 0 with the raw output shown, docs/diagnosis-bug-101.md records reproduce/cause/fix/evidence, and reviews/review-before-merge-bug-101.md completes all seven points of templates/review-before-merge-checklist.md with evidence. Do not commit.
```
