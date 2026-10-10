# Scoped Rules Examples

> **How to use.** Copy any of these files into `.claude/rules/` in your project, for example `.claude/rules/tests.md`. Then edit the `paths:` globs to match your layout. A rule loads only when Claude works with files that match its globs. A rule with no `paths:` loads at the start of every session, just like CLAUDE.md. `paths:` is the only frontmatter key rules support. It takes a YAML list or a comma-separated string of globs, and brace expansion such as `*.{html,js}` works.

| File | Scope (`paths:`) | Purpose |
|---|---|---|
| `tests.md` | `tests/**/*.py` | Test conventions: unittest, isolation, regression naming |
| `api.md` | `notes_api/**/*.py` | Notes API layering, validation, error format, SQL safety |
| `dashboard.md` | `dashboard/**/*.{html,js,css}` | Vanilla JS components, states, accessibility, breakpoints |

**Verify a rule is applied.** Open a file that the rule covers, or ask Claude to edit one, then run `/context`. The rule should appear in the list of loaded content. For a stronger check, ask for a change that the rule constrains, such as "add a test for `shipctl list --owner`". Confirm the result follows the rule; in that case the test should use `unittest` and a temporary `SHIPCTL_DB`.

**Keep rules short.** A rule should be a handful of constraints Claude would otherwise get wrong. Put long procedures in a Skill. If something must always happen, enforce it with a hook.
