# Claude Code Skills Pack (Bootcamp Cohort 2)

Eight ready-to-use `SKILL.md` workflows, two specialist subagents, and three hooks
for taking a change from engineering brief to production readiness decision.
They are written for the workshop project **Shipyard** (`shipctl.py`, `notes_api/`,
`dashboard/`), and you can adapt them to any repository.

Every skill follows the same rules: quote the real command and output, never
invent evidence, never commit or push, and stop at a human decision point.

## What's inside

```
skills-pack/
├── install.sh                      # copy skills/agents/hooks into a project or ~/.claude
├── skills/
│   ├── feature-brief/              # idea -> scope, constraints, acceptance criteria, proof
│   ├── best-of-n-decision/         # + decision-matrix.md, rejected-options-log.md
│   ├── change-review/              # + checklist.md (seven-point Review Before Merge)
│   ├── test-debug-loop/            # failing test -> diagnosis -> fix -> regression evidence
│   ├── browser-verification/       # + checklist.md (flows, console, breakpoints, evidence)
│   ├── security-review/            # + checklist.md (secrets, deps, input, authN/Z, perms, flows)
│   ├── release-readiness/          # + template.md (Production Readiness Report)
│   └── stakeholder-update/         # + template.md (one-page stakeholder update)
├── agents/
│   ├── security-reviewer.md        # read-only (Read, Grep, Glob), severity + file:line + evidence + fix
│   └── test-verifier.md            # Bash limited to test and read-only git commands by a hook
└── hooks/
    ├── block-unsafe-commands.sh    # PreToolUse/Bash: deny destructive or secret-leaking commands
    ├── post-edit-validate.sh       # PostToolUse/Edit|Write: run the relevant tests, exit 2 on failure
    ├── format.sh                   # PostToolUse/Edit|Write: black/prettier only if installed
    ├── settings-snippet.json       # how to wire the hooks in .claude/settings.json
    └── tests/test_hooks.py         # python3 -m unittest discover -s skills-pack/hooks/tests -v
```

| Skill | What it does | Invoke | Model can auto-invoke? |
|-------|--------------|--------|------------------------|
| feature-brief | Converts an idea into outcome, scope, constraints, protected areas, acceptance criteria, and required evidence | `/feature-brief add an --owner filter` | Yes |
| best-of-n-decision | Generates N structurally different designs, scores them on a fixed matrix, and writes a Rejected Options Log | `/best-of-n-decision Notes API storage` | Yes |
| change-review | Applies the seven-point Review Before Merge checklist, with a PASS / FAIL / NOT VERIFIED result per point | `/change-review` | Yes |
| test-debug-loop | Reproduce, diagnose, write a failing regression test, make a bounded fix, verify | `/test-debug-loop updating a note drops its tags` | Yes |
| browser-verification | Chrome-based flow, console, and responsive checks with an evidence log, plus a manual fallback | `/browser-verification http://localhost:8000/ filter by owner` | Yes |
| security-review | Read-only review in a forked `Explore` context; separates verified findings from speculative ones | `/security-review notes_api/` | Yes |
| release-readiness | Production Readiness Report: risk summary, ranked findings, evidence, top 3 fixes, owner, verification, go/no-go | `/release-readiness notes_api` | Yes |
| stakeholder-update | Turns the readiness report and handoff into a one-page business update | `/stakeholder-update docs/readiness.md docs/handoff.md` | **No** (`disable-model-invocation: true`) |

Supporting templates for the whole workshop (CLAUDE.md starter, scoped rules,
decision matrix, report templates) live in [../templates/](../templates/).

## Install

### Option A: install script

```bash
cd skills-pack
./install.sh project ~/src/shipyard                              # skills only, into ~/src/shipyard/.claude/skills/
./install.sh project ~/src/shipyard --with-agents --with-hooks   # plus .claude/agents/ and .claude/hooks/
./install.sh user --with-agents                                  # into ~/.claude/ for all your projects
./install.sh project ~/src/shipyard --dry-run                    # preview
```

- Re-running is safe: identical files are skipped.
- If an installed file differs from the pack version (because you customized it),
  nothing is copied and the script lists the conflicts. Pass `--force` to overwrite.
- `--with-hooks` copies the scripts and **prints** the `settings.json` snippet.
  It never edits your settings files. Paste the snippet into `.claude/settings.json`
  (project) or `~/.claude/settings.json` (user), then check with `/hooks`.

### Option B: copy by hand

```bash
mkdir -p ~/src/shipyard/.claude/skills
cp -r skills/change-review ~/src/shipyard/.claude/skills/      # one skill
cp -r skills/* ~/.claude/skills/                                # all skills, personal
cp agents/*.md ~/src/shipyard/.claude/agents/                   # subagents
```

Project skills (`.claude/skills/`) are shared with everyone who clones the repo.
Personal skills (`~/.claude/skills/`) follow you into every project.

### Option C: install the plugin

`change-review`, `security-review`, the `security-reviewer` agent, and the two
gate hooks are also packaged as the **engineering-quality** plugin. See
[../plugins/engineering-quality/README.md](../plugins/engineering-quality/README.md):

```text
/plugin marketplace add <owner>/claude-code-bootcamp-cohort-2
/plugin install engineering-quality@shipyard-bootcamp
/engineering-quality:change-review
```

### Check it worked

Start `claude` in the project and type `/` to see the skills listed. Ask
"what skills are available?" or run one directly. Claude Code watches skill
directories, so edits to an installed `SKILL.md` apply in the current session
without a restart.

## Customize a skill

Each `SKILL.md` has YAML frontmatter and a Markdown body.

```yaml
---
name: change-review                  # the /command name (defaults to the folder name)
description: Review a ... change ...  # what it does; Claude uses this to decide when to load it
when_to_use: Use when the user says "review this change" ...   # trigger phrases, appended to description
argument-hint: "[optional: brief file, branch, or files]"      # shown in the / menu
allowed-tools: Read Grep Glob Bash(git diff *) Bash(git status *) Bash(git log *)  # pre-approved while it runs
---
```

1. **Description and `when_to_use`.** Write the phrases your team actually uses
   ("ready to ship?", "QA this"). Claude only sees these two fields until the
   skill runs, so they decide automatic discovery. Together they are cut off at
   1,536 characters.
2. **Instructions.** Edit the numbered procedure and the output skeleton. In
   `change-review`, fill in the **Project-specific rules** section (protected
   files, required test commands, extra checks). That is the Part 9 exercise.
3. **Arguments.** `$ARGUMENTS` is replaced with whatever follows the command.
   Use `$0`, `$1` for positional words.
4. **Who can trigger it.** Add `disable-model-invocation: true` for skills only a
   human should start (as in `stakeholder-update`). Add `user-invocable: false` for
   background knowledge Claude should load but users shouldn't call.
5. **Forked context.** `context: fork` plus `agent: Explore` (see
   `security-review`) runs the skill in a separate read-only subagent. A forked
   skill does **not** see your conversation, so pass it a path or range.
   `background: false` makes the turn wait for its result.
6. **Keep keys exact.** Unknown frontmatter keys are silently ignored, so a typo
   such as `allowed_tools` or `disable-model-invokation` just does nothing.
   `claude plugin validate .claude/skills` catches a missing description, but
   not misspelled keys, so proofread key names against the docs.

## Add supporting files

Long reference material belongs in files next to `SKILL.md`. They load only when
the skill links to them and Claude decides it needs them (progressive loading):

```
.claude/skills/change-review/
├── SKILL.md            # short procedure; links to checklist.md
├── checklist.md        # the detailed seven points
└── examples/good-review.md
```

In `SKILL.md`: `Walk the checklist in [checklist.md](checklist.md).` Keep `SKILL.md`
short (these are under 150 lines). Scripts can live in `scripts/` and be
referenced as `${CLAUDE_SKILL_DIR}/scripts/check.sh`.

## Combine with hooks and subagents

- **Hooks are deterministic.** Skills are instructions Claude may follow. Hooks
  always run. Use `post-edit-validate.sh` so tests run after every edit, and
  `block-unsafe-commands.sh` so destructive commands can't run even if a prompt
  goes wrong. Both parse the hook JSON with `python3`, so `jq` isn't needed.
- **Subagents specialize.** `change-review` delegates its security point to
  `security-reviewer` when that agent is installed. To make `security-review`
  run *as* that agent, change `agent: Explore` to `agent: security-reviewer` in
  its frontmatter (requires `--with-agents`).
- **`test-verifier`** shows tool restriction in layers: `tools` omits Edit/Write,
  and a frontmatter `PreToolUse` hook allows only `python3 -m unittest`,
  `node --test`, and read-only `git` commands.

Test the hooks: `python3 -m unittest discover -s skills-pack/hooks/tests -v`.

## Reuse across repositories

- **Personal install** (`./install.sh user`) makes the skills available everywhere.
  If the same skill name exists in both places, the **personal** copy wins over
  the project copy. To customize a skill for one repo, install it in that project
  only, or give the project version a different `name`.
- **Keep project facts out of skills.** Test commands, protected files, and
  conventions go in each repo's `CLAUDE.md`. The skills read it first.
- **Share as a plugin** when a team needs the same versioned workflow in many
  repos (Part 10).
- **Upgrade safely.** Re-run `./install.sh`; it refuses to overwrite your
  customized files unless you pass `--force`. Compare first with `diff -u`.

## Where each skill is used in the workshop

| Skill / asset | Workshop part | Exercise |
|---------------|---------------|----------|
| feature-brief | Part 2: Prompting like a tech lead | Brief for the CLI Release Task Manager |
| feature-brief | Part 6: Git, worktrees, sandboxing | Brief for search and tagging in a worktree |
| best-of-n-decision | Part 4: Best-of-N | Notes API design tournament + Rejected Options Log |
| test-debug-loop | Part 5: Testing, debugging, checkpoints, /goal | Seeded Notes API defect |
| change-review | Part 5 / Part 6 | Review Before Merge checklist; reviewing the worktree diff |
| browser-verification | Part 7: Multimodal + Chrome | Dashboard from a wireframe (manual fallback included) |
| browser-verification | Part 8: Refactor and handoff | Behaviour guardrail during the refactor |
| change-review + security-reviewer + hooks | Part 9: Skills, hooks, subagents | Customize the skill, wire the hook, define the subagent |
| engineering-quality plugin | Part 10: Plugins and marketplaces | Package, validate, install, invoke namespaced |
| change-review, test-verifier | Part 11: Agent Teams | Quality gate before accepting the release-notes feature |
| security-review, release-readiness | Part 12: Production readiness | Production Readiness Report and go/no-go |
| stakeholder-update | Part 13: Cowork | Fallback for learners without Cowork access |

## Caveats

- **Built-in `/security-review`.** Claude Code ships a bundled `/security-review`
  that reviews your branch against `origin`. Installing this pack's
  `security-review` skill **replaces** that command (a custom skill overrides a
  bundled command of the same name). To keep the built-in, rename this skill
  (folder and `name:`, e.g. `shipyard-security-review`), or use the plugin, whose
  version is namespaced as `/engineering-quality:security-review`.
- **Claude in Chrome** needs a paid claude.ai plan, the Chrome extension, and
  `claude --chrome`. It isn't supported in WSL. `browser-verification` includes
  a manual fallback.
- **Hooks run with your permissions.** Read every hook script before you enable it.

License: MIT. Author: Luca Berton.
