# Part 06 · Git workflows, worktrees, permissions and sandboxing

**Project 6: Isolated Search Feature** · 25 minutes · 11:20–11:45 (brief schedule)

## Learning goals
- Use feature branches and focused commits; review Claude-generated diffs
- Isolate experiments with `claude --worktree`
- Run parallel sessions without contaminating the main checkout
- Set filesystem and network boundaries with /sandbox
- Match autonomy to consequence and reversibility

## Learners leave with
- Isolated worktree
- Feature branch
- Search and tagging functionality
- Reviewed diff
- Passing test suite
- Clean merge and commit history

## Run it
```sh
# terminal B (this bootcamp repo)
bin/bootcamp stage 06      # fresh Shipyard repo at ~/shipyard-stage + baseline commit
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
Start `claude --worktree search-tags`, run the prompt, review the diff from main, run the tests yourself in the worktree, then merge and remove the worktree.

## Evidence to show (not claims)
- `git worktree list` shows `.claude/worktrees/search-tags`
- `git diff --stat main...`
- Full suite green inside the worktree
- main untouched while the feature was built
- Merge commit + worktree removed

## Discussion
- What would have happened without the worktree?
- Which commands would you allow in a sandbox, and which network domains?
- When is a branch enough, and when do you want a worktree?

## If it goes wrong
- Load the prepared reference: `bin/bootcamp fallback 06` (say clearly that it is prepared, not live).
- Or jump to the full reference state: `bin/bootcamp checkpoint 06 --force`.
- Play the recorded run in the deck (video `06`): A real worktree session builds search and tags; review the diff from main, then merge.

## Files
- `start/` — overlay that creates the starting state (briefs, inputs)
- `solution/` — overlay that creates the reference checkpoint
- `evidence/` — captured screenshots, outputs and the recorded Claude Code run (`recorded-run/`)
