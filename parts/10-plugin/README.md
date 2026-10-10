# Part 10 · Plugins and marketplace distribution

**Project 9B: Package the Engineering Quality Plugin** · 25 minutes · 13:55–14:20 (brief schedule)

## Learning goals
- Package Skills, hooks, subagents and MCP configuration as one plugin
- Write the manifest; understand namespacing
- Validate (`claude plugin validate --strict`), install and test locally
- Distribute through a marketplace; version, trust and maintain

## Learners leave with
- Validated Claude Code plugin
- Local plugin installation
- Successful namespaced invocation
- Distribution README

## Run it
```sh
# terminal B (this bootcamp repo)
bin/bootcamp stage 10      # fresh Shipyard repo at ~/shipyard-stage + baseline commit
# terminal A
cd ~/shipyard-stage && claude --model sonnet
# ... paste the prompts from PROMPTS.md ...
# terminal B
bin/bootcamp verify           # acceptance checks on ~/shipyard-stage
```

## Timing inside the part
- 4 min: topic slides
- 5 min: live demo or recorded video (deck)
- 6 min: explain and discuss
- rest: hands-on lab

## Lab
Package, validate with --strict, install from the local marketplace, run `/engineering-quality:change-review`.

## Evidence to show (not claims)
- `claude plugin validate … --strict` → Validation passed
- `claude plugin install engineering-quality@shipyard-tools`
- `claude plugin details` inventory and token cost
- Namespaced skill output

## Discussion
- What would you put in a plugin, and what stays in CLAUDE.md?
- How do you trust a plugin from another team?
- When do you bump the version?

## If it goes wrong
- Load the prepared reference: `bin/bootcamp fallback 10` (say clearly that it is prepared, not live).
- Or jump to the full reference state: `bin/bootcamp checkpoint 10 --force`.
- Play the recorded run in the deck (video `10`): Plugin packaged and validated, installed from a local marketplace, invoked by its namespaced name.

## Files
- `start/` — overlay that creates the starting state (briefs, inputs)
- `solution/` — overlay that creates the reference checkpoint
- `evidence/` — captured screenshots, outputs and the recorded Claude Code run (`recorded-run/`)
