# Post-release routine brief: Shipyard daily verification

| Field | Decision |
|---|---|
| **Trigger** | Daily at 08:45 for 7 days after each release (cloud routine via `/schedule`); also on merge to `main` (GitHub event trigger) |
| **Scope** | Repository `shipyard`, branch `main` only. Read access to code and test output. No production data. |
| **Required permissions** | Read files; run `python3 -m unittest …`, `node --test …`, `python3 seed.py --force` in the routine's own checkout; open a draft issue or post a comment. No push, no merge, no deploy, no secrets. |
| **Expected output** | A short report: test totals (raw summary lines), readiness-probe results (bind address, CORS header, oversized-request behaviour), new TODO/FIXME since the last run, and a one-line verdict: GREEN / YELLOW / RED. |
| **Human approval point** | Any proposed fix is opened as a draft PR or issue for the engineer of record. The routine never merges or edits `main`. |
| **Completion / stop condition** | Stop after 7 consecutive GREEN runs, or immediately after the first RED (open an issue tagged `release:v1.4`, notify the release manager, disable the routine until a human re-enables it). Hard limit: 15 minutes per run. |

## Local vs cloud
- Cloud routine: tests and probe on a fresh clone. Safe because they need no local credentials.
- Stays local (Remote Control): anything needing the VPN, the shared VM, or local credentials (e.g. checking the real deployment).

## Why these stop conditions
Routines run autonomously with no permission prompts, so the brief has to make the safe outcome the default: read-only scope, draft-only output, and a stop rule that hands control back to a human.
