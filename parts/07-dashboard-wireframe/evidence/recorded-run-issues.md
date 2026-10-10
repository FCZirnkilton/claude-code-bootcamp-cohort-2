# Recorded run: what the browser check showed

The recorded headless run (`recorded-run/turn1.jsonl`) built the dashboard from `wireframes/release-dashboard.png` and the brief. Headless runs cannot drive Claude in Chrome, so the browser step was captured afterwards with headless Chromium on the same seeded data (`seed.py`).

| Check | Result | Evidence |
|---|---|---|
| Layout follows the wireframe (header, 4 KPI cards, tasks table, notes with chips) | Pass | `recorded-run/claude-built-desktop-1280.png` |
| KPI values match the seeded data (6 open, 2 done, 2 overdue, 5 notes) | Pass | same screenshot |
| Overdue due dates in red | Pass | rows "Rotate staging credentials", "Run load test on Notes API" |
| Browser console at 1280 px and 390 px | Pass: no messages | Playwright console capture `[]` |
| Mobile 390 px | Rendered; see screenshot | `recorded-run/claude-built-mobile-390.png` |
| Note bodies escaped | Yes: `**bold**` shows literally (no HTML injection) | desktop screenshot, notes panel |
| Target date | "not set": the wireframe gives no date, and Claude did not invent one | header badge |

Differences from the reference checkpoint: the recorded build uses a light, sketch-like theme taken directly from the wireframe and escapes note bodies; the reference uses the dark Shipyard theme and renders `**bold**` (which Part 12 flags as a stored-XSS risk).
