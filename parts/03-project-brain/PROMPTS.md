# Part 03 prompts

Copy each block into Claude Code in order. Read the output before sending the next one.

## 1. Write the project brain

```text
Create a concise CLAUDE.md for this repository (under 60 lines): stack, exact build and test commands, conventions you can infer from shipctl.py and tests/, the exit-code contract, protected files (SAFETY.md, .claude/settings.json, briefs/), and do-not rules. Then create two path-scoped rules with `paths:` frontmatter: .claude/rules/tests.md for tests/**/*.py and .claude/rules/cli.md for shipctl.py. Keep anything occasional out of CLAUDE.md. Do not commit.
```

## 2. Prove the context is applied

```text
Add a `shipctl stats` command that prints pending, done and overdue counts per owner. Follow CLAUDE.md and the rules in .claude/rules. When done, list which specific rules you applied and where, run the full test suite and show the raw output. Do not commit.
```
