# Part 14 prompts

Copy each block into Claude Code in order. Read the output before sending the next one.

## 1. Remote Control (`claude --remote-control "Shipyard v1.4 verification"`)

```text
Run both test suites and evidence/readiness_probe.py, then write a five-line verification status to ops/remote-verification-status.md: test totals with the raw summary lines, probe results, verdict GREEN/YELLOW/RED and the next step. Stop after writing the file; do not edit anything else.
```

## 2. Design the routine

```text
Write ops/post-release-routine.md using templates/post-release-routine-brief.md: a recurring post-release check for this repository with trigger, repository scope, required permissions (least privilege), expected output, the human approval point, and the completion or stop condition. Say what must stay local and what can run as a cloud routine.
```
