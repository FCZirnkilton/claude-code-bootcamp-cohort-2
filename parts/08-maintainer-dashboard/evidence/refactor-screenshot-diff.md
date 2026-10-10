# Refactor guardrail: before/after screenshot diff

Captured with headless Chromium (Playwright) against the same seeded data, before (part 07 checkpoint) and after (part 08 checkpoint) the refactor.

| Viewport | Before | After | Pixel diff bounding box |
|---|---|---|---|
| Desktop 1280 px | `../../07-dashboard-wireframe/evidence/dashboard-desktop-1280.png` | `after-refactor-desktop-1280.png` | (382, 1263, 404, 1272) |
| Mobile 390 px | `../../07-dashboard-wireframe/evidence/dashboard-mobile-390.png` | `after-refactor-mobile-390.png` | (53, 1986, 74, 1995) |

The only differing pixels are inside the footer's "updated HH:MM:SS" timestamp, which changes on every load. Layout, data and styling are identical. Browser console: no messages in either run. `node --test dashboard/tests/`: 7 pass, 0 fail.
