# Claude Code Bootcamp Cohort 2: workshop materials

Materials repository for a 7.5-hour Packt workshop. The learners' product (Shipyard) is assembled from overlays in `parts/`.

## Commands
- All checks: `bin/bootcamp preflight` (builds every checkpoint and runs its tests)
- One part: `bin/bootcamp checkpoint NN --dir /tmp/x --force && bin/bootcamp verify --dir /tmp/x`
- Regenerate runbooks after editing `tools/course_data.py`: `python3 tools/gen_parts.py`
- Skills Pack hook tests: `python3 -m unittest discover -s skills-pack/hooks/tests -q`
- Mock test tests: `python3 -m unittest discover -s mock-test/tests -q`
- Plugin: `claude plugin validate ./plugins/engineering-quality --strict` and `claude plugin validate . --strict`
- Deck: `python3 deck/build_deck.py` (python-pptx + ffmpeg); videos: `python3 deck/video/render_run.py NN`

## Conventions
- `tools/course_data.py` is the single source of truth for timings, prompts, goals, evidence and discussion. Edit there, then regenerate; never hand-edit `parts/*/README.md` or `PROMPTS.md`.
- Part N's starting state = all previous `start/` + `solution/` overlays + part N `start/`. A `.delete` file in an overlay removes paths.
- Shipyard code: Python 3.10+ standard library only; dashboard is plain ES modules, no build step, no npm dependencies.
- Every claim in a document is backed by real evidence: quote the command and its output. Never write invented test counts, findings or run narratives.
- Speaker notes in the deck are first-person recitation scripts.
- Feature syntax must match `docs/FEATURE-REFERENCE.md` (verified against the official docs); re-verify after Claude Code upgrades.

## Do not
- Do not commit recordings scratch directories (`~/bootcamp-recordings`) or `deck/.posters/`.
- Do not edit `docs/BRIEF.md` (verbatim copy of the client brief).
- Do not put secrets or personal tokens anywhere in this repository.
