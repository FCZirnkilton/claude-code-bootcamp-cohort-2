# Scenario-Based Knowledge Quiz

**Weight:** 30% of the assessment. 25 questions, 1.2 points each, 30 points total.
**Time:** 40 minutes. **Format:** single best answer (A to D). Workshop materials and Claude Code docs are allowed. Work individually.

Each question describes a situation on the Shipyard project. Choose the **best** response: the one a careful engineer of record would choose, not just one that would technically work.

---

## Permissions and safety

**1.** You are starting Project 2. You want Claude to run the unit tests without prompting, ask before every commit, and never read `.env`. Which `.claude/settings.json` configuration does this?

- A. `allow: ["Bash(*)"]`, `deny: ["Read(./.env)"]`
- B. `allow: ["Bash(python3 -m unittest *)", "Bash(git commit *)"]`, `deny: ["Read(./.env)"]`
- C. `allow: ["Bash(python3 -m unittest *)"]`, `ask: ["Bash(git commit *)"]`, `deny: ["Read(./.env)"]`
- D. No rules. Write "never read .env and ask before committing" in CLAUDE.md, and use `bypassPermissions` for speed.

**2.** Your PreToolUse hook for `Bash` prints `Blocked: rm not allowed` to stderr and exits with code 1. Claude still ran `rm -rf build/`. What is the most likely reason?

- A. PreToolUse hooks cannot block Bash commands; only PostToolUse hooks can.
- B. Exit code 1 is a non-blocking error. To block, the hook must exit with code 2 (or return a `deny` permission decision).
- C. Hooks must write to stdout, not stderr, to be seen.
- D. Hooks only run when the session is in plan mode.

**3.** A teammate finds permission prompts annoying during the dashboard refactor and wants to run Claude with `bypassPermissions` on their laptop. What is the best response?

- A. That is fine, as long as CLAUDE.md tells Claude to be careful.
- B. That is fine, as long as git is initialized, because `/rewind` can restore anything.
- C. Use `dontAsk` instead; it behaves the same but shows fewer messages.
- D. `bypassPermissions` is meant for isolated containers or VMs. On a laptop, reduce prompts with targeted `allow` rules (or `acceptEdits`/`auto` mode) and keep the deny rules and a recovery point.

**4.** A product manager says: "Have Claude fix whatever is broken in the Notes API and deploy it tonight." Which delegation is safest while still useful?

- A. "Investigate the failing tests and propose a fix plan. Work on a feature branch and change only `notes_api/` and `tests/`. Run the full suite. Do not touch deployment configuration or credentials. Stop for my review before merging or deploying."
- B. "Fix everything and deploy, but be careful."
- C. "Fix everything in auto mode. If tests fail, run `git reset --hard` and try again until they pass, then deploy."
- D. "Do not use Claude for this. Production-related work must be done entirely by hand."

**5.** Claude generated a data-import script for the Notes API. You want to run it but make sure it can write only inside the project and cannot reach the network. What enforces this best?

- A. Add "do not access the network or write outside the repo" to CLAUDE.md.
- B. Add `Edit` deny rules for every path outside the project.
- C. Enable the sandbox (`/sandbox`, or `"sandbox": {"enabled": true}`) and configure the filesystem write paths and network allowed domains, so the operating system enforces the limits on Bash commands and their child processes.
- D. Switch to plan mode before running the script.

## Feature selection

**6.** Your test conventions (use `unittest`, use a temporary `SHIPCTL_DB`, name regression tests after the bug) only matter when Claude works in `tests/`. Where should they go?

- A. A "Testing" section in the root CLAUDE.md.
- B. `.claude/rules/tests.md` with `paths:` frontmatter matching `tests/**/*.py`.
- C. A PostToolUse hook.
- D. An MCP server.

**7.** The team wants a validation script to run after **every** file edit Claude makes, with no exceptions. What should you use?

- A. A PostToolUse hook with matcher `Edit|Write` that runs the script.
- B. A line in CLAUDE.md: "Always run the validation script after edits."
- C. A Skill named `validate`.
- D. An auto memory entry.

**8.** You have a 250-line release-readiness procedure that is used once per release. CLAUDE.md is already long. Where should the procedure go?

- A. Append it to CLAUDE.md so it is always available.
- B. Put it in `.claude/rules/release.md` with no `paths:` frontmatter.
- C. Save it to auto memory.
- D. Move it into a Skill, such as `.claude/skills/release-readiness/SKILL.md`, with a clear description, so the full body loads only when it is used.

**9.** You want an independent security review of the new search endpoint. The reviewer should be able to read code but not edit it, and its judgment should not be shaped by the conversation that wrote the code. What fits best?

- A. Ask the main session: "Now review your own code for security issues."
- B. Launch an Agent Team with three teammates.
- C. A `security-reviewer` subagent in `.claude/agents/` with read-only tools (for example `tools: Read, Grep, Glob`) and a focused description.
- D. A hook that blocks commits.

**10.** You need to fix a typo in `shipctl --help` and add one test for it. What is the most appropriate setup?

- A. An Agent Team with frontend, backend, and test owners.
- B. A single Claude Code session, ideally with a short brief.
- C. Three parallel worktrees, with Best-of-N on the typo.
- D. A scheduled cloud routine.

**11.** You want to share the `change-review` Skill, the post-edit validation hook, and the security-reviewer subagent across six repositories, with versioned updates. What should you do?

- A. Copy the `.claude/` folder into each repository by hand.
- B. Put everything in `~/.claude/CLAUDE.md`.
- C. Wrap them in an MCP server.
- D. Package them as a plugin (`engineering-quality`) with `skills/`, `hooks/hooks.json`, and `agents/`, validate it with `claude plugin validate`, and distribute it through a marketplace with versions.

**12.** During triage, Claude needs to read live tickets from your team's issue tracker. What is the right mechanism?

- A. Connect the tracker through an MCP server and scope its tools with permission rules (for example `mcp__tracker__*`).
- B. Paste a weekly export of the tickets into CLAUDE.md.
- C. A SessionStart hook that prints every ticket.
- D. A rule file with `paths:` frontmatter.

**13.** You installed the `engineering-quality` plugin locally. How do you invoke its `change-review` Skill?

- A. `/change-review`
- B. `/plugin change-review`
- C. `/engineering-quality:change-review`
- D. `@engineering-quality`

## Context

**14.** Shipyard's CLAUDE.md has grown to 420 lines, and Claude now regularly ignores your naming conventions. What is the best fix?

- A. Add "IMPORTANT" in capitals to every rule.
- B. Trim CLAUDE.md to project-wide essentials. Move path-specific guidance into `.claude/rules/` with `paths:`, move procedures into Skills, and enforce must-always behavior with hooks. Then check what loads with `/context`.
- C. Copy the same content into `CLAUDE.local.md` as well.
- D. Switch to a larger model.

**15.** After you migrated from pytest to `unittest`, Claude keeps running `pytest`. `/memory` shows an auto memory entry: "Tests run with pytest." What should you do?

- A. Edit or remove the stale entry through `/memory`, make sure CLAUDE.md states the correct test command, and confirm the fix in a new session.
- B. Turn off auto memory permanently for all projects.
- C. Ignore it, because CLAUDE.md always overrides memory.
- D. Delete the repository's `.claude/` directory.

**16.** During a failed experiment, Claude ran `rm tests/test_tags.py` through Bash. You used `/rewind` and chose **Restore code**, but the file did not come back. Why?

- A. Checkpoints keep only the last 10 prompts.
- B. You needed **Restore conversation** instead.
- C. Checkpoints stop working after a session is resumed.
- D. Checkpoints track Claude's file edits, not changes made by Bash commands such as `rm`, `mv`, or `cp`. Recover the file from git.

**17.** You want Claude to keep working on BUG-101 until it is genuinely done. Which `/goal` is best?

- A. `/goal make the Notes API production quality`
- B. `/goal keep working until you are confident the bug is fixed`
- C. `/goal python3 -m unittest discover -s tests exits 0 and test_title_only_patch_keeps_body is reported ok`
- D. `/goal run the tests every 5 minutes for the next hour`

## Security and evidence

**18.** Claude's final message says "All 31 tests pass." The transcript contains no test run. What do you do?

- A. Accept it; Claude probably ran the tests in the background.
- B. Treat it as a claim, not evidence. Run the test command yourself (or have Claude run it), keep the raw output and exit code, and only then mark Tests as passing.
- C. Ask Claude "Are you sure?" and accept a yes.
- D. Mark Tests as N/A in Review Before Merge.

**19.** A review tool flags "possible SQL injection in `repository.py`". You check, and every query uses `?` placeholders; none builds SQL from strings. How should this appear in your Production Readiness Report?

- A. As a speculative concern that was not reproduced, citing the parameterized queries as evidence, with an optional verification test. Do not rank it as a High finding.
- B. Rank it Critical, because every security finding is critical.
- C. Delete the review output so it does not confuse stakeholders.
- D. Rewrite the repository to use a different database.

**20.** A learner pasted a real GitHub token into CLAUDE.md so Claude could call the API, and committed it to a feature branch that has not been pushed yet. What is the correct response?

- A. That is fine, because the branch has not been pushed.
- B. Move the token into `CLAUDE.local.md` and keep using it.
- C. Delete the line in a new commit, and you are done.
- D. Treat the token as exposed. Revoke or rotate it, remove it from git history before any push, provide credentials through an environment variable or connector instead, and add deny rules for secret files.

## Workflow decisions

**21.** For the Notes API tournament, Claude proposes three designs. All three are layered SQLite services; they differ only in folder names and in whether the service is a class or a set of functions. What should you do?

- A. Score them and pick the winner; that is Best-of-N.
- B. Reject them as cosmetic variants. Ask for designs that differ in storage, consistency, or layering (for example a single-module JSON store, layered SQLite, and an event-sourced log), then score them against the fixed criteria.
- C. Merge all three into a hybrid that takes the best part of each.
- D. Ask Claude which one it prefers, and use that one.

**22.** You need to add search and tags to the Notes API while the main checkout stays stable, because you are still fixing a bug on `main`. What should you do?

- A. Work directly on `main` and commit often.
- B. Stash the bug fix and build search on `main`.
- C. Start an isolated worktree, for example `claude --worktree search-tags`. Review the diff and run the tests there before merging.
- D. Copy the repository folder to `/tmp` and work there without git.

**23.** The Agent Team lead is in plan mode, and you assume the lead will review each teammate's plan before any edits happen. What should you know?

- A. The docs state that teammate plans are auto-approved without the lead reviewing them. Add an explicit human approval step ("present every plan to me and wait") and keep quality gates such as a `TaskCompleted` hook.
- B. The `TeammateIdle` hook approves plans automatically after reviewing them.
- C. Teammates always ask the human to approve every file edit, whatever the settings.
- D. Plan mode prevents teammates from ever editing files.

**24.** You start `/remote-control`, go to lunch, and close your laptop lid. On your phone, the session stops making progress. Why?

- A. Remote Control only works with API keys.
- B. Remote Control requires `claude --cloud`.
- C. The mobile app can only view sessions, not steer them.
- D. Remote Control steers a session that still runs locally, so the `claude` process and the machine must stay awake and online. For work that should continue while the laptop sleeps, push the branch and use a cloud session instead.

**25.** You are designing a daily post-release routine. Routines run in the cloud, autonomously, with no permission prompts. Which design is safest?

- A. If the tests fail, the routine reverts the last commit on `main` and redeploys.
- B. The routine runs the tests read-only and reports the status. If something is unhealthy, it opens one issue containing the raw output. A human decides on any revert or hotfix. If a check cannot run, it never reports healthy.
- C. Give the routine production credentials so it can check live data and fix problems.
- D. A stop condition is unnecessary, because routines are rate-limited.

---

*Answer key: instructor only (`quiz-answer-key.md`).*
