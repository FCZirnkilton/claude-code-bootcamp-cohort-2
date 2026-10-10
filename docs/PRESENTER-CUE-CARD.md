# Presenter cue card: Claude Code Bootcamp Cohort 2

**Deck:** `deck/claude-code-bootcamp-cohort-2.pptx` (videos embedded; every slide has first-person speaker notes).
**Timings:** `docs/RUN-OF-SHOW.md`. **Per-part runbooks:** `parts/NN-*/README.md`. **Prompts:** `parts/NN-*/PROMPTS.md`.

## 30 minutes before
1. `bin/bootcamp preflight` → `PREFLIGHT PASSED` (tools + all 14 checkpoints).
2. `claude --version` and `/status`: logged in, Sonnet available. `claude update` the day before, not the morning of.
3. Open the deck, start the slideshow, click the Part 1 video for two seconds, Esc. Videos are silent: share screen without computer audio.
4. Chrome with the Claude in Chrome extension connected (`claude --chrome`, then `/chrome` → status) for Part 7.
5. `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` exported in the terminal you will use for Part 11. tmux installed if you want split panes.
6. Remote Control enabled for your org (Part 14) and the Claude mobile app logged in.
7. Terminal font at 20 pt or more; two terminals: A = Claude Code in `~/shipyard-stage`, B = this repo.

## The rhythm of every part
Section → goals → concepts → **prompt slide** (read it aloud) → **video slide** (click to play; “recording of a real run of these exact prompts”) → evidence → **discuss** → **lab** (`bin/bootcamp stage NN`) → checkpoint.
Live instead of video: paste the same prompt in terminal A. If it runs long: switch to the video, or `bin/bootcamp fallback NN` and say “prepared reference, not generated live”.

## Lines worth saying exactly
- Part 1: “Autonomy is proportional to reversibility.”
- Part 2: “‘Tests pass’ is a claim. ‘Ran 15 tests … OK’ is evidence.”
- Part 4: “The most valuable line in a Rejected Options Log is when the loser would win.”
- Part 5: “The failing test is the contract the fix must satisfy.”
- Part 8: “The only pixels that changed are the clock.”
- Part 9: “If a rule must never be broken, it is a hook, not an instruction.”
- Part 10: “The plugin's own review caught the plugin's missing chmod.”
- Part 12: “Conditional go, with owners and verification actions.”
- Close: “Build faster. Orchestrate smarter. Verify everything. Ship with confidence.”

## Plan-dependent features (say it up front)
| Part | Feature | Without access |
|---|---|---|
| 7 | Claude in Chrome (Pro/Max/Team/Enterprise, extension ≥ 1.0.36, not WSL) | `templates/browser-verification-checklist.md` + `parts/07-dashboard-wireframe/evidence/` |
| 11 | Agent Teams (experimental, env var) | recorded transcript + task board + `bin/bootcamp diff 11` |
| 13 | Cowork (paid plan, desktop app) | `/stakeholder-update` skill from `skills-pack/` |
| 14 | Remote Control (claude.ai login; Team/Enterprise owner must enable) | design the routine with the template |

## Recovery at any time
```sh
bin/bootcamp fallback NN            # load the prepared solution into ~/shipyard-stage
bin/bootcamp checkpoint NN --force  # jump to the end of part NN
```
Never present a fallback or a recording as live-generated.

## After the session
Point learners to `skills-pack/install.sh`, `assessment/README.md` and `python3 mock-test/run.py`. Read the disclaimer slide verbatim.
