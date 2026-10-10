# Part 09 prompts

Copy each block into Claude Code in order. Read the output before sending the next one.

## 1. Specialist review

```text
Use the security-reviewer subagent to review notes_api/ and dashboard/js/. It must cite file:line and quoted evidence for every finding and rank them by severity. Save its report to reviews/security-review-dashboard.md. Do not change any code.
```

## 2. Hook in action

```text
Make the release target date in dashboard/index.html read 2026-11-12 instead of 2026-11-10 and tell me what the post-edit validation hook reported. Then test our PreToolUse guardrail: the block-unsafe-commands hook is expected to stop secret reads before they run. Attempt exactly `cat .env` once (the file may not even exist) and report the hook's message word for word. Do not try any workaround.
```
