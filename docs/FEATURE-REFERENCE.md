# Claude Code feature reference (official docs, fetched 2026-10-10)

**Sources and caveats.** I fetched every page as raw markdown from `https://code.claude.com/docs/en/<page>.md`, using the index at `https://code.claude.com/docs/llms.txt`. The docs cite versions up to about v2.1.295, and many behaviours depend on version. Before the workshop, run `claude update` and check `claude --version`.

---

## 1. Skills (`/en/skills`)

**Locations:**
- Personal: `~/.claude/skills/<name>/SKILL.md`
- Project: `.claude/skills/<name>/SKILL.md`. Parent directories up to the repo root also load. Nested `.claude/skills/` folders load lazily, once Claude touches files there.
- Plugin: `<plugin>/skills/<name>/SKILL.md`, invoked as `/plugin-name:skill-name`.
- Others: an enterprise copy in the managed settings dir, `--add-dir` directories, and skills synced from your claude.ai account (`/anthropic-skills:<name>`).
- Don't name a skill folder `synced`; that name is reserved.

**Frontmatter.** All keys are optional; `description` is recommended. Keys are lowercase and hyphenated. Unknown keys are silently ignored.

| Key | Values and notes |
|---|---|
| `name` | Command name; defaults to the directory name |
| `description` | Combined with `when_to_use`, truncated at 1,536 characters in the listing |
| `when_to_use` | Trigger phrases, appended to the description |
| `argument-hint` | e.g. `[issue-number]` |
| `arguments` | Named positional args, e.g. `[issue, branch]`, used as `$issue` and `$branch` |
| `disable-model-invocation` | `true` means only the user can invoke it. Default `false` |
| `user-invocable` | `false` hides it from the `/` menu so only Claude can invoke it. Default `true` |
| `allowed-tools` | Pre-approves tools for the invoking turn only, e.g. `Bash(git add *) Bash(git commit *)` |
| `disallowed-tools` | Removes tools while the skill is active |
| `model` | Any `/model` value, or `inherit` |
| `effort` | `low`, `medium`, `high`, `xhigh`, `max` |
| `context` | `fork` runs the skill as a subagent |
| `agent` | Subagent type for a fork, e.g. `Explore`, `Plan`, `general-purpose` or a custom agent. Default `general-purpose` |
| `background` | Only with `context: fork`. **Default `true`**; set `false` to block the turn until it finishes |
| `hooks` | Same format as settings hooks |
| `paths` | Globs; the skill auto-loads only for matching files |
| `shell` | `bash` or `powershell` |
| `metadata`, `license`, `compatibility` | Accepted but not acted on |

**Arguments:**
- `$ARGUMENTS` is the full argument string.
- `$ARGUMENTS[0]` or `$0` are 0-based positional args with shell-style quoting.
- `$name` comes from the `arguments` list.
- If no placeholder exists, Claude Code appends `ARGUMENTS: <value>`.
- Variables: `${CLAUDE_SKILL_DIR}`, `${CLAUDE_SESSION_ID}`, `${CLAUDE_EFFORT}`, `${CLAUDE_PROJECT_DIR}`, and in plugins `${CLAUDE_PLUGIN_ROOT}` and `${CLAUDE_PLUGIN_DATA}`.
- `` !`cmd` `` injects command output into the skill before Claude reads it.

**Progressive loading:**
- Only the description sits in context; the full body loads when the skill is invoked.
- Supporting files such as `reference.md` and `scripts/` load only when `SKILL.md` links to them. Keep `SKILL.md` under 500 lines.
- After compaction, Claude Code re-attaches the first 5k tokens of each invoked skill, within a 25k total budget.

**Skills vs slash commands:**
- `.claude/commands/*.md` is the older format and still works.
- It takes the same frontmatter except `name` and `paths`.
- Subfolders become namespaces: `commands/frontend/x.md` is `/frontend:x`.
- Skills are preferred for new work.

**Example (`.claude/skills/fix-issue/SKILL.md`):**
```yaml
---
description: Fix a GitHub issue by number
disable-model-invocation: true
argument-hint: [issue-number]
allowed-tools: Bash(gh issue view *)
---
Fix GitHub issue $ARGUMENTS following our standards. Write tests, then commit.
```

## 2. Subagents (`/en/sub-agents`)

**Locations, in priority order:**
1. Managed settings
2. The `--agents '<json>'` flag
3. `.claude/agents/` (scanned recursively; walks up to the repo root)
4. `~/.claude/agents/`
5. A plugin's `agents/` directory (subfolders become part of the ID, e.g. `my-plugin:review:security`)

**Frontmatter.** Keys are camelCase. Only `name` and `description` are required.

| Key | Values and notes |
|---|---|
| `name`, `description` | Required. `name` must not contain `:` |
| `tools` | Comma string or YAML list; inherits all tools if omitted |
| `disallowedTools` | Tools to remove |
| `model` | `sonnet`, `opus`, `haiku`, `fable`, a full model ID, or `inherit` |
| `permissionMode` | `default`, `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions`, `plan`, or the alias `manual` |
| `maxTurns` | Turn limit |
| `skills` | Full skill content is preloaded; skills with `disable-model-invocation: true` can't be preloaded |
| `mcpServers`, `hooks` | A `Stop` hook here becomes `SubagentStop` |
| `memory` | `user` → `~/.claude/agent-memory/<name>/`; `project` → `.claude/agent-memory/<name>/`; `local` → `.claude/agent-memory-local/<name>/` |
| `background` | `true` forces the background |
| `effort` | Effort level |
| `isolation` | `worktree` |
| `omitClaudeMd` | Skips user/project/local CLAUDE.md |
| `color` | Display colour |
| `initialPrompt` | First turn when run as the session agent |
| `experimental.cacheTtl` | `5m` or `1h` |

Plugin agents ignore `hooks`, `mcpServers` and `permissionMode`.

**How to invoke:**
- Name the agent in natural language.
- `@"code-reviewer (agent)"` or `@agent-<name>` forces that agent for one task.
- `claude --agent code-reviewer`, or `"agent": "code-reviewer"` in settings, makes it the whole-session agent.
- `/agents` now only prints a reminder to ask Claude or edit the files. On v2.1.197 and earlier it opened a wizard.

**Background:**
- Interactive sessions have "fork mode" on by default, so spawned subagents run in the background.
- Ctrl+B backgrounds a running task; `/tasks` lists them.
- Background subagents get a smaller tool set, and their permission prompts surface in the main session.
- `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1` forces the foreground.
- `/subtask <task>` forks the full conversation as a background subagent (v2.1.212+).

**Nested subagents:**
- On by default, up to 3 layers deep.
- Change the depth with `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`; `1` turns nesting off.
- At most 20 run concurrently (`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`).
- `Agent(worker, researcher)` in `tools` is an allowlist that only applies with `claude --agent`. The Task tool was renamed Agent in v2.1.63.

## 3. Hooks (`/en/hooks`)

**Events:** SessionStart, Setup, UserPromptSubmit, UserPromptExpansion, PreToolUse, PermissionRequest, PermissionDenied, PostToolUse, PostToolUseFailure, PostToolBatch, Notification, MessageDisplay, SubagentStart, SubagentStop, TaskCreated, TaskCompleted, Stop, StopFailure, TeammateIdle, InstructionsLoaded, ConfigChange, CwdChanged, DirectoryAdded, FileChanged, WorktreeCreate, WorktreeRemove, PreCompact, PostCompact, PreModelSwitch, PostModelSwitch, Elicitation, ElicitationResult, SessionEnd.

**Where hooks live:**
- `~/.claude/settings.json`, `.claude/settings.json`, `.claude/settings.local.json`, managed settings.
- A plugin's `hooks/hooks.json`.
- Skill frontmatter: active for the rest of the session once invoked; `once: true` is honoured only here.
- Agent frontmatter: active only while that subagent runs.

**Schema:** `{"hooks": {"<Event>": [{"matcher": "...", "hooks": [{"type": "command", "command": "..."}]}]}}`
- `type` is one of `command`, `http`, `mcp_tool`, `prompt`, `agent`.
- Common fields: `if` (permission-rule syntax, e.g. `"Bash(git *)"`, tool events only), `timeout` (default 600 s for command), `statusMessage`, `once`.
- Command-only fields: `args`, `async`, `asyncRewake`, `shell`, `onFailure: "block"` (v2.1.295+).

**Matchers:**
- `*`, empty or omitted matches everything.
- Letters, digits, `_`, `-`, `|` and `,` mean an exact match or a list, e.g. `Edit|Write`.
- Any other character makes it an unanchored JS regex, e.g. `mcp__memory__.*` or `^Edit$`.
- SessionStart matches `startup`, `resume`, `clear`, `compact`, `fork`.
- UserPromptSubmit and Stop don't support matchers.

**Stdin JSON:** `session_id`, `prompt_id`, `transcript_path`, `cwd`, `permission_mode`, `hook_event_name`, and for tool events `tool_name`, `tool_input` and `tool_use_id`. `agent_id` and `agent_type` are present inside subagents.

**Exit codes:**
- `0`: success; stdout JSON is parsed. Plain stdout becomes context only on UserPromptSubmit, UserPromptExpansion, SessionStart and PostModelSwitch.
- `2`: blocking error; stderr goes to Claude.
- Anything else: non-blocking error. Exit 1 does **not** block; use 2 to enforce a policy.

**JSON output:**
- Universal fields: `continue`, `stopReason`, `systemMessage`, `terminalSequence`.
- Top-level `decision: "block"` plus `reason` applies to UserPromptSubmit, PostToolUse, Stop, SubagentStop and others.
- PreToolUse instead uses `hookSpecificOutput`:
  - `permissionDecision`: `allow`, `deny`, `ask`, or `defer` (defer works in `-p` only)
  - `permissionDecisionReason`, `updatedInput`, `additionalContext`
  - When hooks disagree, precedence is deny > defer > ask > allow.
  - The old top-level `approve`/`block` for PreToolUse is deprecated.

**Example: blocking `rm` in Bash (`.claude/settings.json`):**
```json
{"hooks":{"PreToolUse":[{"matcher":"Bash","hooks":[{"type":"command","command":"\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/no-rm.sh"}]}]}}
```
```bash
#!/bin/bash
cmd=$(jq -r '.tool_input.command' <<<"$(cat)")
[[ "$cmd" == rm* ]] && { echo "Blocked: rm not allowed" >&2; exit 2; }
exit 0
```

**Plugin hooks:** `hooks/hooks.json` must wrap the event map in a top-level `"hooks"` key. Use `"${CLAUDE_PLUGIN_ROOT}"` in commands.

**Other controls:** `/hooks` is a read-only browser. `"disableAllHooks": true` turns hooks off.

## 4. Plugins (`/en/plugins/create`, `/en/plugins/manifest-reference`, `/en/plugins/marketplace-reference`, `/en/plugins/dependencies`, `/en/plugins/loading`)

**Layout:**
- `.claude-plugin/plugin.json` is optional, and only the manifest goes inside `.claude-plugin/`.
- At the plugin root: `skills/<n>/SKILL.md`, `commands/`, `agents/`, `hooks/hooks.json`, `.mcp.json`, `.lsp.json`, `output-styles/`, `workflows/`, `themes/`, `monitors/monitors.json`, `bin/` (added to PATH), `settings.json` (only `agent` and `subagentStatusLine` apply).
- A root `CLAUDE.md` is **not** loaded.

**plugin.json:**
- Only `name` is required (kebab-case; no `claude-` or `anthropic-` prefixes).
- Optional: `displayName`, `version`, `description`, `author{name,email,url}`, `homepage`, `repository`, `license`, `keywords`, `defaultEnabled`, `dependencies`, `userConfig`, `settings`, `channels`, `metadata`, and the component paths `skills`, `commands`, `agents`, `hooks`, `mcpServers`, `lspServers`, `outputStyles`, `workflows`, `experimental`.
- Components are namespaced: `/my-plugin:review`, agent `my-plugin:reviewer`.

**Validate and test:**
- `claude plugin validate ./my-plugin` (add `--strict` to fail on warnings).
- `claude --plugin-dir ./my-plugin`; repeat the flag for more plugins; `.zip` files work.
- `/reload-plugins` picks up edits.
- `claude plugin init <name>` scaffolds a plugin in `~/.claude/skills/` that loads as `<name>@skills-dir`.
- `CLAUDE_CODE_PLUGIN_DIRS` loads plugins without the flag (v2.1.280+).

**Marketplace (`.claude-plugin/marketplace.json`):**
- Required: `name`, `owner{name}`, and `plugins[]` entries with `name` and `source`.
- `source` types: relative `./path`, `github`, `url`, `git-subdir`, `npm`, `archive`, `command`.
- Install loop:
  - `claude plugin marketplace add ./my-marketplace` (or `/plugin marketplace add ./path` in a session)
  - `claude plugin install my-first-plugin@my-marketplace`
  - `claude plugin list` to confirm

**Versioning:**
- A `version` in the manifest wins over the marketplace entry; setting it pins users until you change it.
- With no version, git sources use the 12-character commit SHA.
- `dependencies` accepts `"name"`, `"name@marketplace"`, or `{name, version: "~2.1.0", marketplace}`. Ranges resolve against git tags (`claude plugin tag`).

## 5. Permissions, sandbox, trust (`/en/permission-modes`, `/en/permissions`, `/en/sandboxing`)

**Modes:**

| Mode | Behaviour |
|---|---|
| `default` | Labelled **Manual**; `manual` is an alias |
| `acceptEdits` | Auto-accepts edits and common filesystem commands |
| `plan` | No edits until you approve a plan |
| `auto` | A classifier reviews actions instead of prompting |
| `dontAsk` | Anything not pre-approved is denied; not in the Shift+Tab cycle |
| `bypassPermissions` | Containers and VMs only |

- **Auto mode is now the built-in starting mode** for interactive terminal and VS Code sessions on v2.1.283+.
- Auto mode needs a supported model: Opus/Sonnet 4.6+, Haiku 5.5 or Fable on the Anthropic API.
- `defaultMode: "auto"` works only from `~/.claude/settings.json`, not project files.
- Admins can turn modes off with `permissions.disableAutoMode` or `disableBypassPermissionsMode` set to `"disable"`.
- Switch modes with Shift+Tab, `--permission-mode <mode>`, or `permissions.defaultMode`.

**Rule syntax:**
- Rules are `Tool` or `Tool(specifier)` in `permissions.allow`, `ask` and `deny`. Evaluation order is deny, then ask, then allow.
- Bash examples: `Bash(npm run *)`, `Bash(git commit *)`. Put the `*` after the subcommand. `Bash(ls:*)` is the same as `Bash(ls *)`.
- Read/Edit rules use gitignore patterns:
  - `//abs/path` is absolute.
  - `~/path` is under home.
  - `/path` is relative to the settings file's location.
  - `./path` or `path` is relative to the current directory.
- Other forms: `WebFetch(domain:x.com)`, `mcp__server__*`, `Agent(isolation:worktree)`.
- `/permissions` opens the rules UI.

**Sandbox:**
- Off by default. Turn it on with `/sandbox` (tabs: Mode auto-allow/regular, Overrides, Config) or `"sandbox": {"enabled": true}`.
- Runs on macOS (Seatbelt) and Linux/WSL2 (needs `bubblewrap` and `socat`). Native Windows is unsupported.
- Keys:
  - `sandbox.filesystem.allowWrite`, `denyWrite`, `denyRead`, `allowRead`
  - `sandbox.network.allowedDomains`, `deniedDomains`
  - `excludedCommands`, `allowUnsandboxedCommands`, `autoAllowBashIfSandboxed`, `failIfUnavailable`
- Sandbox paths use normal conventions (`/tmp/x`, `~/x`), unlike permission rules.

**Workspace trust:**
- Project `permissions.allow` rules and `additionalDirectories` apply only after you accept the trust dialog.
- `-p` never shows the dialog.
- Trust is stored in `~/.claude.json` as `projects["<path>"].hasTrustDialogAccepted`.

**Settings precedence (highest first):** managed > `--settings` > `.claude/settings.local.json` > `.claude/settings.json` > `~/.claude/settings.json`.

## 6. Memory (`/en/memory`)

**CLAUDE.md locations:**
- Managed: `/etc/claude-code/CLAUDE.md` on Linux, `/Library/Application Support/ClaudeCode/CLAUDE.md` on macOS.
- User: `~/.claude/CLAUDE.md`.
- Project: `./CLAUDE.md` or `./.claude/CLAUDE.md`.
- Local: `./CLAUDE.local.md`.

Files in parent directories load at launch; subdirectory files load on demand.

**Imports:** `@path/to/file`, relative to the importing file, up to 4 hops deep. Imports outside the project trigger an approval dialog. Imports inside code spans are ignored.

**Rules:**
- `.claude/rules/**/*.md` (project) and `~/.claude/rules/` (user).
- The only frontmatter key is **`paths:`**, a YAML list or comma string of globs; brace expansion works.
- Rules without `paths` load at launch.

**Auto memory:**
- On by default, stored at `~/.claude/projects/<project>/memory/`, shared across the repo's worktrees.
- Contains a `MEMORY.md` index (first 200 lines or 25KB load each session) plus topic files.
- Turn it off with the `/memory` toggle, `"autoMemoryEnabled": false`, or `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`.
- Relocate it with `autoMemoryDirectory`.
- `/memory` lists and opens files and toggles auto memory. `/context` shows what loaded.

## 7. Checkpointing (`/en/checkpointing`) and `/goal` (`/en/goal`)

**Rewind:**
- Open the menu with `/rewind` (aliases `/checkpoint`, `/undo`) or Esc Esc on an empty prompt.
- Options: **Restore code and conversation**, **Restore conversation**, **Restore code**, **Summarize from here**, **Summarize up to here**, **Never mind**.
- A checkpoint is taken for each prompt that starts a turn; the last 100 are kept, and they survive resume.

**Not restored:**
- Bash-made changes (`rm`, `mv`, `cp`)
- External edits
- Most subagent edits, including background forked skills and background `/code-review --fix`
- Symlinked or hard-linked files
- It's not a replacement for git.

**`/goal` exists:**
- Set a goal: `/goal all tests in test/auth pass and lint is clean` (max 4,000 characters). It starts a turn immediately.
- `/goal` alone shows status (turns, tokens, last reason). `/goal clear` removes it; aliases are `stop`, `off`, `reset`, `none`, `cancel`.
- One goal per session; it's restored on resume.
- How completion is judged: it's a session-scoped prompt-based Stop hook. After each turn the small fast model returns **not yet met**, **met** or **impossible**.
- The evaluator reads only the transcript and doesn't run tools, so phrase conditions Claude can demonstrate, e.g. "`npm test` exits 0".
- It doesn't change the permission mode; pair it with auto mode for unattended runs.
- `claude -p "/goal ..."` also works.
- Unavailable when hooks are disabled or `allowManagedHooksOnly` is set.

## 8. Worktrees (`/en/worktrees`)

- `claude --worktree feature-auth` (or `-w`) creates `.claude/worktrees/<name>/` on branch `worktree-<name>`. A name is generated if you omit it.
- `--tmux` opens a tmux session for it. `-w #123` or a PR URL branches the worktree from that PR.
- Interactive use needs workspace trust. Add `.claude/worktrees/` to `.gitignore`.
- Worktrees branch from the remote default branch. `"worktree": {"baseRef": "head"}` branches from local HEAD instead.
- `.worktreeinclude` (gitignore syntax) copies gitignored files such as `.env` into new worktrees.

**Cleanup:**
- On exit, a clean unnamed worktree is removed automatically. If there's work, you're prompted to keep or remove it; resume with `claude --worktree <name> --resume`.
- `-p` runs are never cleaned up; use `git worktree remove`.
- `isolation: worktree` on a subagent gives it a temporary worktree, deleted if there are no changes. Otherwise a periodic sweep removes it after `cleanupPeriodDays`.

## 9. Agent Teams (`/en/agent-teams`)

**Status:** experimental and off by default. Enable with `"env": {"CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"}` or the same variable in your shell.

**Lead and teammates:**
- The main session is the lead and stays the lead.
- Teammates are separate Claude Code instances with their own context windows.
- While teams are enabled, any subagent Claude spawns with a `name` launches as a teammate.

**Shared state:**
- Task list at `~/.claude/tasks/{team}/`, with pending, in-progress and completed states, dependencies, and file-lock claiming.
- Mailbox at `~/.claude/teams/{team}/inboxes/{agent}.json`.
- You can message teammates directly: arrow keys plus Enter in in-process mode, Ctrl+T toggles the task list, `x` stops a teammate.

**Plan approval:**
- Teammates spawned while the lead is in plan mode work read-only until their plan is ready.
- **Docs say Claude Code auto-approves the plan without the lead reviewing it.**

**Display:**
- `teammateMode` setting or `--teammate-mode`: `in-process` (default), `auto`, `tmux`, or `iterm2`.
- Split panes need tmux or iTerm2 with the `it2` CLI. Not supported in the VS Code terminal, Windows Terminal or Ghostty.

**Quality-gate hooks:** `TeammateIdle`, `TaskCreated`, `TaskCompleted`.

**Limitations:**
- `/resume` and `/rewind` don't restore in-process teammates.
- Task status can lag.
- One team per session; no nested teams.
- Permissions are fixed at spawn.

**Cost:** significantly more tokens, scaling with the number of teammates.

## 10. Claude in Chrome (`/en/chrome`)

**Prerequisites:**
- Chrome, Edge, or another Chromium browser (Brave, Arc, …).
- The Claude in Chrome extension, version 1.0.36 or later.
- A Pro, Max, Team or Enterprise plan, signed in with `/login`. API keys and `setup-token` don't work.
- Not available on Bedrock, Vertex or Foundry, and not supported in WSL.

**Usage:**
- `claude --chrome`.
- `/chrome` shows status, manages permissions, reconnects, selects a browser, and has an **Enabled by default** option (which uses more context).

**Capabilities:**
- Navigate, click and type.
- Read console errors and the DOM.
- Use your logged-in sites.
- Fill forms, upload files, extract data.
- Record GIFs and save screenshots to disk.

**Limitations:**
- It pauses on logins and CAPTCHAs.
- JS modal dialogs block it.
- The extension service worker can idle out; fix with `/chrome` → "Reconnect extension".
- Site permissions come from the extension.

## 11. Remote Control and cloud (`/en/remote-control`, `/en/claude-code-on-the-web`)

**Remote Control requirements:**
- Pro, Max, Team or Enterprise. On Team and Enterprise an Owner must enable it in the admin settings.
- claude.ai login; no API keys.
- Not available on Bedrock, Vertex, Foundry, or with a custom `ANTHROPIC_BASE_URL`.
- `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` must not be set.

**How to start it:**
- `claude remote-control` is server mode. Flags: `--name`, `--spawn same-dir|worktree|session`, `--capacity`, `-c`, `--permission-mode`. Press spacebar for a QR code.
- `claude --remote-control "Name"` (or `--rc`) starts an interactive session with Remote Control on.
- `/remote-control` (or `/rc`) inside a session carries the existing conversation over.

**Connecting:** open the session URL, scan the QR code, or find the session in claude.ai/code or the mobile app's Code tab. It still runs locally, so the `claude` process must stay alive. `/plugin` and `/resume` are local-only.

**Cloud sessions:**
- `claude --cloud "task"` starts one (`--remote` is a deprecated alias). It clones your GitHub remote, so push first.
- Available on Pro, Max and Team, and on Enterprise with premium or Chat + Claude Code seats.
- Handoff is one-way, from cloud to terminal: `claude --teleport [id]`, or `/teleport` / `/tp` in a session. Teleport needs a clean git state, the same repo, and a pushed branch.

## 12. Routines, scheduling, Cowork (`/en/routines`, `/en/scheduled-tasks`, `/en/desktop-scheduled-tasks`)

**Routines:**
- Research preview; Pro, Max, Team and Enterprise.
- They run in the cloud and are managed at claude.ai/code/routines or with `/schedule` (alias `/routines`).
- Examples: `/schedule daily PR review at 9am`, `/schedule tomorrow at 9am, ...`. Manage with `/schedule list`, `/schedule update`, `/schedule run`.
- Triggers: schedule (minimum 1 hour; use a custom cron via `/schedule update`), API (bearer token, set up on the web), GitHub events.
- They run autonomously with no permission picker.
- Limits: 100 scheduled runs per hour per account. They use subscription usage.

**Other scheduling:**
- `/loop [interval] [prompt]`, e.g. `/loop 5m check the deploy`. It needs the session open and expires after 7 days.
- Desktop scheduled tasks run locally while the app is open, with a minimum interval of 1 minute.

**Cowork:**
- code.claude.com only mentions it. Its docs are at `claude.com/docs/cowork/overview`: "agentic workspace" in Claude Desktop, built on the Claude Code architecture.
- It reads skills and plugins enabled for your claude.ai account, not `~/.claude`.
- **I could not confirm Cowork plan requirements or Cowork-specific scheduled tasks**; the overview page doesn't state them.

## 13. Code review (`/en/code-review`, `/en/ultrareview`, `/en/commands`)

**Local review:**
- `/code-review [low|medium|high|xhigh|max|ultra] [--fix] [--comment] [--max-findings n|all|default] [pr#|branch|path]`.
- **`/review` is now an alias of `/code-review`** (since v2.1.223).
- It runs as a background forked subagent. `--fix` edits aren't undone by `/rewind`.

**`/security-review`:** reviews the branch diff against origin's default branch. It needs an `origin` remote.

**Code Review (managed GitHub service):**
- Research preview, **Team and Enterprise only**. Not available with ZDR or HIPAA.
- An Owner sets it up at claude.ai/admin-settings/claude-code, which installs the Claude GitHub App.
- Trigger it with `@claude review` or `@claude review always` on a PR. Tune it with `REVIEW.md` or `CLAUDE.md`.
- Costs about $15–25 per review, billed as usage credits.

**Ultrareview:**
- Run `/code-review ultra [base|PR#]`; `/ultrareview` is an alias.
- From scripts or CI: `claude ultrareview [PR|base]`.
- Runs in the cloud and needs a claude.ai login. Not on Bedrock, Vertex, Foundry, ZDR or HIPAA.
- Pro and Max get 3 free runs, once only; after that it costs $5–25 per run in usage credits.
- The docs don't state Team or Enterprise pricing.

## 14. Output styles, effort, model, context, background (`/en/output-styles`, `/en/model-config`, `/en/commands`, `/en/agent-view`)

**Output styles:**
- Built-ins: Default, Proactive, Concise, Explanatory, Learning.
- Switch with `/output-style <name>` (v2.1.269+), via `/config`, or with `"outputStyle": "Explanatory"`. The setting value is case-sensitive.
- Custom styles go in `~/.claude/output-styles/` or `.claude/output-styles/*.md`.
- Custom style frontmatter: `name`, `description`, `keep-coding-instructions`, and `force-for-plugin` (plugins only).

**Effort:**
- Levels: `low`, `medium`, `high`, `xhigh`, `max`.
- Opus 5.5, Sonnet 5.5 and Haiku 5.5 default to `medium`; most other models default to `high`.
- Set it with `/effort <level|auto>`, `--effort`, `CLAUDE_CODE_EFFORT_LEVEL`, `effortLevel` / `modelSettings`, or skill/agent frontmatter.
- `max` lasts for the session only.
- `ultrathink` in a prompt asks for deeper reasoning on that one turn.
- `ultracode` is a separate toggle for dynamic workflows (`/effort ultracode`).

**Model:**
- `/model [alias|name]` saves your default; press `s` in the picker to switch for this session only. Also `--model`, `ANTHROPIC_MODEL`, or the `model` setting.
- Aliases: `default`, `best`, `fable`, `sonnet`, `opus`, `haiku`, `sonnet[1m]`, `opus[1m]`, `opusplan`.

**Context:**
- `/context [all]` shows a usage grid.
- `/compact [instructions]` summarises the conversation.

**Background sessions and agent view (research preview):**
- `claude agents` opens agent view.
- `claude --bg "task"` starts a background session; `--agent`, `--name` and `--resume <id>` all work with it.
- `/background` (or `/bg`) detaches the current session.
- `/fork` copies the session to the background.
- Background sessions auto-isolate into worktrees. Turn that off with `worktree.bgIsolation: "none"`.
