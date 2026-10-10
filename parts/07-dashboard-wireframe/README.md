# Part 07 · Multimodal building and Chrome verification

**Project 7: Dashboard from a Wireframe** · 25 minutes · 11:55–12:20 (brief schedule)

## Learning goals
- Turn a wireframe into components, states and interaction requirements
- Improve the prompt before patching generated UI by hand
- Connect Claude Code to Chrome (`claude --chrome`, /chrome)
- Test navigation and forms, inspect the console, check responsive layouts, capture evidence
- Convert findings into focused fixes

## Learners leave with
- Working dashboard
- Componentized frontend
- Browser verification evidence
- Console and interaction issue log
- Before-and-after status for identified issues

## Run it
```sh
# terminal B (this bootcamp repo)
bin/bootcamp stage 07      # fresh Shipyard repo at ~/shipyard-stage + baseline commit
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
Build from the wireframe, then verify with `claude --chrome`. No Chrome? Use the browser verification checklist and the captured evidence in parts/07/evidence.

## Evidence to show (not claims)
- Component/state list extracted from the image
- Desktop and 390 px screenshots
- Console: no errors
- Issue log with before/after

## Discussion
- What did Claude extract from the annotations that you would have missed?
- Which issues can only be found in a real browser?
- When do you fix the prompt instead of patching the UI?

## If it goes wrong
- Load the prepared reference: `bin/bootcamp fallback 07` (say clearly that it is prepared, not live).
- Or jump to the full reference state: `bin/bootcamp checkpoint 07 --force`.
- Play the recorded run in the deck (video `07`): Claude reads the wireframe, builds the dashboard and verifies it; real screenshots at 1280 and 390 px.
- Availability: Claude in Chrome needs the Chrome extension and a claude.ai login. Without it, use `templates/browser-verification-checklist.md` with the captured screenshots in `evidence/`.

## Files
- `start/` — overlay that creates the starting state (briefs, inputs)
- `solution/` — overlay that creates the reference checkpoint
- `evidence/` — captured screenshots, outputs and the recorded Claude Code run (`recorded-run/`)
