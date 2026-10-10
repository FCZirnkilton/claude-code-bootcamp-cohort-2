# Shipyard

Shipyard is a small release-management toolkit built live during the Claude Code Bootcamp (Cohort 2).
Python 3 standard library and plain HTML/JavaScript only. No package installs.

The human who reviews and merges a change is the engineer of record. Claude proposes; the engineer of record decides.

## shipctl: release task manager

```sh
python3 shipctl.py add "Freeze public API" --owner maya --due 2026-11-05
# Added #1: Freeze public API
python3 shipctl.py add "Write release notes"
python3 shipctl.py assign 2 omar
python3 shipctl.py due 2 2026-11-02
python3 shipctl.py list                       # pending, by due date
python3 shipctl.py list --owner maya --status all
python3 shipctl.py done 1
python3 shipctl.py delete 2
```

| Command | Purpose |
|---|---|
| `add <title> [--owner O] [--due YYYY-MM-DD]` | add a release task |
| `assign <id> <owner>` | set the owner |
| `due <id> <YYYY-MM-DD>` | set the due date |
| `list [--owner O] [--status pending\|done\|all]` | list tasks (default: pending) |
| `done <id>` | mark completed |
| `delete <id>` | delete |

Data lives in `./tasks.json`; set `SHIPCTL_DB=/path/file.json` to use another file.
Exit codes: `0` success, `1` user error, `2` storage error.

## Tests

```sh
python3 -m unittest discover -s tests -q
```
