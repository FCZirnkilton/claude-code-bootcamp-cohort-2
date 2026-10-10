# Part 09 · Skills, hooks and specialist subagents

**Project 9A: Engineering Quality Skills Pack** · 35 minutes · 13:20–13:55 (brief schedule)

## Learning goals
- Choose between CLAUDE.md, rules, Skills, hooks, MCP, subagents and Agent Teams
- Read SKILL.md structure: description, discovery, arguments, supporting files, forked context
- Use hooks as deterministic controls: post-edit tests, blocking unsafe commands
- Create specialist subagents with restricted tools

## Learners leave with
- Customized SKILL.md
- Working post-edit validation hook
- Specialist subagent definition
- Structured review output

## Run it
```sh
# terminal B (this bootcamp repo)
bin/bootcamp stage 09      # fresh Shipyard repo at ~/shipyard-stage + baseline commit
# terminal A
cd ~/shipyard-stage && claude --model sonnet
# ... paste the prompts from PROMPTS.md ...
# terminal B
bin/bootcamp verify           # acceptance checks on ~/shipyard-stage
```

## Timing inside the part
- 5 min: topic slides
- 7 min: live demo or recorded video (deck)
- 8 min: explain and discuss
- rest: hands-on lab

## Lab
Customize the description and add a Shipyard section to change-review/SKILL.md, wire the hooks in settings.json, then run the two prompts.

## Evidence to show (not claims)
- `/hooks` lists PreToolUse and PostToolUse
- Post-edit tests run automatically
- `git push --force` blocked with the hook's reason
- Severity-ranked review with file:line

## Discussion
- Which rule in your team should be a hook, not an instruction?
- Why does the security reviewer get only Read, Grep and Glob?
- What would make a skill trigger automatically, and when should it not?

## If it goes wrong
- Load the prepared reference: `bin/bootcamp fallback 09` (say clearly that it is prepared, not live).
- Or jump to the full reference state: `bin/bootcamp checkpoint 09 --force`.
- Play the recorded run in the deck (video `09`): Read-only security reviewer finds the stored XSS with file:line; the hook blocks a force push.

## Files
- `start/` — overlay that creates the starting state (briefs, inputs)
- `solution/` — overlay that creates the reference checkpoint
- `evidence/` — captured screenshots, outputs and the recorded Claude Code run (`recorded-run/`)
