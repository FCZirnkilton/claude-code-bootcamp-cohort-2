# Permission Boundary

> **How to use.** Fill this in during Project 1, before you let Claude Code do any autonomous work. Write it for the repository you are about to trust. Then encode the allowed, ask, and blocked lines as `permissions` rules in `.claude/settings.json`, and create the recovery point at the bottom. Review it each time you raise autonomy, for example when you switch to `acceptEdits` or `auto` mode, enable the sandbox, or start a worktree or background session.
>
> Rule of thumb: match autonomy to consequence and reversibility. Claude may do reversible, local work freely. Anything irreversible, shared, or external needs a human, and that human is the engineer of record.

---

## 1. Workspace

| Field | Value |
|---|---|
| Repository / path | `__________` |
| Engineer of record (human) | `__________` |
| Permission mode for this work | `default` (Manual) / `acceptEdits` / `plan` / `auto`. Use `bypassPermissions` only inside a container or VM |
| Sandbox | off / on (filesystem: `____`, network: `____`) |
| Workspace trust accepted | yes / no |
| Date | `__________` |

## 2. Actions

| Category | Action | Reversible? | How it is enforced |
|---|---|---|---|
| Allowed (no prompt) | `__________` | yes | `permissions.allow` rule |
| Ask first | `__________` | partly | `permissions.ask` rule |
| Blocked | `__________` | no | `permissions.deny` rule, plus a PreToolUse hook where a rule is not enough |

Guidance:
- **Allowed**: read-only commands, running tests, and edits inside the working tree on a feature branch.
- **Ask**: commits, new dependencies, edits to protected files, network access.
- **Blocked**: reading secrets, pushing to shared branches, force-pushes, history rewrites, deleting data outside the repo, deploys, and production credentials.

## 3. Protected areas

| Path or resource | Why it is protected | Allowed interaction |
|---|---|---|
| `__________` | `__________` | read-only / none |

## 4. Recovery point

| Field | Value |
|---|---|
| Baseline commit hash | `__________` |
| Tag or branch | `__________` |
| Verified clean `git status` | yes / no |
| How to restore | `__________` |

Note: `/rewind` restores Claude's own file edits. It does **not** undo changes made through Bash (`rm`, `mv`, `cp`), external edits, or most subagent edits, so it is not a replacement for git. Make the git recovery point before any autonomous run.

## 5. Stop conditions

Claude must stop and ask the engineer of record when: `__________`

---

## Example: Shipyard, Project 1

**Workspace.** The repository is `~/work/shipyard` and the engineer of record is Dana Ruiz. Mode: `default` (Manual) for Project 1, then `acceptEdits` on feature branches from Project 2 onward. The sandbox is on for Project 6. Workspace trust has been accepted.

| Category | Action | Reversible? | Enforcement |
|---|---|---|---|
| Allowed | `python3 -m unittest discover -s tests` | yes | `Bash(python3 -m unittest *)` |
| Allowed | `git status`, `git diff`, `git log` | yes | `Bash(git status)`, `Bash(git diff *)`, `Bash(git log *)` |
| Allowed | Edit files under `shipctl.py`, `notes_api/`, `tests/` on a feature branch | yes (git) | mode `acceptEdits` |
| Ask | `git commit` | yes | `Bash(git commit *)` in `ask` |
| Ask | `git push` to a feature branch | partly | `Bash(git push *)` in `ask` |
| Blocked | Read `.env` and other secret files | n/a | `Read(./.env)`, `Read(./.env.*)` in `deny` |
| Blocked | Force-push, `git reset --hard` | no | `Bash(git push --force *)`, `Bash(git reset --hard *)` in `deny` |
| Blocked | `rm -rf` | no | `Bash(rm -rf *)` in `deny`, plus the unsafe-command PreToolUse hook (exit code 2) |

`.claude/settings.json`:

```json
{
  "permissions": {
    "allow": [
      "Bash(python3 -m unittest *)",
      "Bash(git status)",
      "Bash(git diff *)",
      "Bash(git log *)"
    ],
    "ask": [
      "Bash(git commit *)",
      "Bash(git push *)"
    ],
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Bash(git push --force *)",
      "Bash(git reset --hard *)",
      "Bash(rm -rf *)"
    ]
  }
}
```

Rules are evaluated in the order deny, then ask, then allow. A command that matches a deny rule is blocked even if an allow rule also matches it.

**Protected areas.** `.env` (no access), `tasks.json` and `notes.db` (local data: read-only for Claude), `.github/` (read-only).

**Recovery point.** Baseline commit `3f2c9a1`, tagged `baseline-p1`. `git status` was clean. To restore, run `git switch main && git reset --hard baseline-p1`. The human runs that command; Claude does not.

**Stop conditions.** Claude stops on any request to touch `.env`, any new dependency (the project is stdlib only), any test failure it cannot explain, and any change outside the files named in the brief.
