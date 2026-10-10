# Part 12 prompts

Copy each block into Claude Code in order. Read the output before sending the next one.

## 1. Production review

```text
Read briefs/production-review.md. Run /engineering-quality:security-review on notes_api/ and dashboard/js/, then review the rest yourself. Write reports/production-readiness.md with: risk summary, severity-ranked findings each with evidence (file:line, config, test or runtime output you actually ran), a separate list of speculative concerns, top three fixes with owner and verification action, and a Go / Conditional go / No-go recommendation. Do not fix anything.
```
