# CLAUDE.md Starter

> **How to use.** Copy the template block into `./CLAUDE.md` (or `./.claude/CLAUDE.md`) at the repository root and fill it in. Aim for **under 60 lines**. Claude loads it in every session, so every line costs context and dilutes the others. After saving it, start a new session, run `/context` to confirm it loaded, and ask Claude to make a small change that should follow one of your conventions. That change is your evidence that the file works.

## What belongs here
- **Stack:** language, runtime, and the few libraries that matter.
- **Commands:** the exact build, test, lint, and run commands.
- **Conventions:** project-wide rules Claude would otherwise get wrong.
- **Do-not:** protected files and forbidden actions.
- **Glossary:** domain terms with a project-specific meaning.

## What does NOT belong here
| Content | Put it here instead |
|---|---|
| Rules that apply to one directory or file type | `.claude/rules/<topic>.md` with `paths:` frontmatter |
| Long procedures used only sometimes (release checklist, review steps) | A Skill (`.claude/skills/<name>/SKILL.md`) |
| Something that must happen every time (formatting, blocking `rm -rf`) | A hook; CLAUDE.md is guidance, not enforcement |
| Secrets, tokens, internal URLs with credentials | Nowhere in the repo; use environment variables |
| Personal preferences | `~/.claude/CLAUDE.md` or `./CLAUDE.local.md` |
| Full API docs or architecture essays | `docs/`, linked with `@docs/architecture.md` only if needed every session |
| Things Claude learns as it works | Auto memory; review it with `/memory` |

## Template

```markdown
# <Project name>

<One sentence: what this project is and who uses it.>

## Stack
- <language + version>, <framework or "stdlib only">
- <data store>

## Commands
- Test: `<command>`
- Run: `<command>`
- Lint/format: `<command>`

## Conventions
- <convention 1>
- <convention 2>
- Every behavior change ships with a test.

## Do-not
- Do not read or edit <secret files>.
- Do not modify <protected paths>.
- Do not add dependencies without asking.

## Glossary
- **<term>**: <meaning in this project>
```

## Example: Shipyard (under 40 lines)

```markdown
# Shipyard

Release-management toolkit: `shipctl` CLI, Notes API, and a release dashboard.

## Stack
- Python 3 standard library only (no pip installs)
- Vanilla HTML/CSS/JS dashboard, no build step
- SQLite via `sqlite3` for the Notes API; JSON file for shipctl

## Commands
- All tests: `python3 -m unittest discover -s tests -v`
- Notes API: `python3 -m notes_api.server` (port 8000, `NOTES_DB` sets the file)
- Dashboard: `python3 -m http.server 8080 -d dashboard`
- shipctl: `python3 shipctl.py --help` (`SHIPCTL_DB` sets the file)

## Conventions
- Notes API layering: `server.py` (HTTP only) -> `service.py` (validation) -> `repository.py` (SQL only)
- Parameterized SQL only; never build SQL with string formatting
- Errors to clients are JSON `{"error": "..."}`; never return tracebacks
- Every bug fix starts with a failing regression test named after the bug
- Small, focused commits on feature branches; never commit to `main` directly

## Do-not
- Do not read or edit `.env` or any `*.db` / `tasks.json` data file
- Do not modify `.github/` or `docs/BRIEF.md`
- Do not add third-party dependencies
- Do not push, force-push, or rewrite history

## Glossary
- **Release task**: a shipctl item with owner, due date, and status pending/done
- **Note**: Notes API record (id, title, body, tags, created_at, updated_at)
- **Engineer of record**: the human accountable for merging a change
- **Review Before Merge**: our seven-point checklist; see the change-review Skill
```
