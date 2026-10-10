# Part 11 prompts

Copy each block into Claude Code in order. Read the output before sending the next one.

## 1. Launch the team (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`)

```text
Read briefs/release-notes-team.md. Create an agent team with three teammates: backend owner, frontend owner, and test and verification owner, each restricted to the files listed in the brief. Require plan approval before any teammate edits. Freeze the API contract from the brief first, write the task list with dependencies to docs/team-plan.md, then let the teammates work in parallel. When all tasks are done, run both test suites, show the raw output, and summarise what each teammate changed. Do not commit.
```

## 2. Steer one teammate

```text
Message the frontend owner: the panel must show an empty-state message when the release has no notes, and the Copy button must say "Copied" for 1.5 seconds.
```
