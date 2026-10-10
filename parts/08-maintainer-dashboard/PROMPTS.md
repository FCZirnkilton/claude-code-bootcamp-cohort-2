# Part 08 prompts

Copy each block into Claude Code in order. Read the output before sending the next one.

## 1. Bounded refactoring plan (plan mode)

```text
Read REFACTOR-REQUEST.md. Propose a bounded refactoring plan for dashboard/app.js: target modules and their single responsibility, what will not change (HTML ids, API calls, rendering, behaviour), and how the existing tests and a browser check prove behaviour is preserved. Do not edit yet.
```

## 2. Implement, re-verify, hand off

```text
Plan approved. Implement it. Keep the existing test assertions (only import paths may change), run both test suites and show the raw output. Then write docs/ARCHITECTURE.md (one page), docs/HANDOFF.md (start here, how to change things safely, known limitations, ownership) and update README.md. Do not commit.
```
