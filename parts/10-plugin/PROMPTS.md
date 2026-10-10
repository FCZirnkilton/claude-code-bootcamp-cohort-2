# Part 10 prompts

Copy each block into Claude Code in order. Read the output before sending the next one.

## 1. Package

```text
Read briefs/package-plugin.md. Package our .claude/ change-review skill, a security-review skill, the security-reviewer agent and both hooks into plugins/engineering-quality/ with a valid .claude-plugin/plugin.json and hooks/hooks.json using ${CLAUDE_PLUGIN_ROOT}. Add the marketplace file .claude-plugin/marketplace.json named shipyard-tools. Run claude plugin validate on both with --strict and show the output. Do not commit.
```

## 2. Namespaced invocation (`claude --plugin-dir ./plugins/engineering-quality`)

```text
/engineering-quality:change-review briefs/package-plugin.md
```
