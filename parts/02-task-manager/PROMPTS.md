# Part 02 prompts

Copy each block into Claude Code in order. Read the output before sending the next one.

## 1. Plan first (plan mode)

```text
Read briefs/cli-release-task-manager.md and SAFETY.md. Propose an implementation plan for shipctl: files, functions, storage format, how each acceptance criterion will be tested, and the risks. Do not write code yet.
```

## 2. Implement after approval

```text
Plan approved. Implement shipctl.py, tests/test_shipctl.py and the README section exactly as planned. Run python3 -m unittest discover -s tests -v and show the raw output. Then give me a table mapping every acceptance criterion (AC1-AC8) to the test that proves it, and a short terminal session with real CLI output for AC1, AC4 and AC5 using SHIPCTL_DB=./demo-tasks.json. Do not commit.
```
